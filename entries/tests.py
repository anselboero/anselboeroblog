from django.test import TestCase

from .models import Entry, Person, Quote
from .quotes import extract_quotes


class ExtractQuotesTests(TestCase):
    """Unit tests for the pure markdown parser (no DB)."""

    def test_extracts_attributed_blockquote(self):
        body = (
            "Intro.\n\n"
            "> Real artists ship.\n"
            ">\n"
            "> — [Steve Jobs](/people/steve-jobs/)\n"
        )
        quotes = extract_quotes(body)
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]['text'], 'Real artists ship.')
        self.assertEqual(quotes[0]['slug'], 'steve-jobs')
        self.assertEqual(quotes[0]['source_url'], '')
        self.assertEqual(quotes[0]['order'], 0)

    def test_plain_blockquote_is_ignored(self):
        body = "> Just a quote with no attribution link.\n"
        self.assertEqual(extract_quotes(body), [])

    def test_attribution_line_is_stripped_from_text(self):
        body = (
            "> Stay hungry, stay foolish.\n"
            "> — [Steve Jobs](/people/steve-jobs/)\n"
        )
        quotes = extract_quotes(body)
        self.assertEqual(quotes[0]['text'], 'Stay hungry, stay foolish.')

    def test_captures_source_url_from_other_link(self):
        body = (
            "> Real artists ship.\n"
            "> — [Steve Jobs](/people/steve-jobs/) · [folklore](https://folklore.org/x)\n"
        )
        quotes = extract_quotes(body)
        self.assertEqual(quotes[0]['source_url'], 'https://folklore.org/x')

    def test_absolute_person_url_is_matched(self):
        body = "> Hi.\n> — [SJ](https://example.com/people/steve-jobs/)\n"
        quotes = extract_quotes(body)
        self.assertEqual(quotes[0]['slug'], 'steve-jobs')

    def test_multiple_quotes_preserve_document_order(self):
        body = (
            "> First.\n> — [A](/people/a/)\n\n"
            "> Second.\n> — [B](/people/b/)\n"
        )
        quotes = extract_quotes(body)
        self.assertEqual([q['text'] for q in quotes], ['First.', 'Second.'])
        self.assertEqual([q['order'] for q in quotes], [0, 1])

    def test_multiline_quote_text_is_joined(self):
        body = (
            "> Line one\n"
            "> line two.\n"
            ">\n"
            "> — [Steve Jobs](/people/steve-jobs/)\n"
        )
        quotes = extract_quotes(body)
        self.assertEqual(quotes[0]['text'], 'Line one\nline two.')


class SyncOnSaveTests(TestCase):
    """Integration tests for the post_save signal that syncs Quote rows."""

    def setUp(self):
        self.person = Person.objects.create(name='Steve Jobs', slug='steve-jobs')

    def _entry(self, body, **kwargs):
        return Entry.objects.create(
            title='T', slug='t', body=body, is_published=True, **kwargs
        )

    def test_quote_created_and_linked(self):
        entry = self._entry(
            "> Real artists ship.\n> — [Steve Jobs](/people/steve-jobs/)\n"
        )
        quote = entry.quotes.get()
        self.assertEqual(quote.text, 'Real artists ship.')
        self.assertEqual(quote.person, self.person)

    def test_person_added_to_entry_people(self):
        entry = self._entry("> Hi.\n> — [Steve Jobs](/people/steve-jobs/)\n")
        self.assertIn(self.person, entry.people.all())

    def test_unknown_slug_is_skipped(self):
        entry = self._entry("> Hi.\n> — [Ghost](/people/ghost/)\n")
        self.assertEqual(entry.quotes.count(), 0)

    def test_resave_replaces_quotes(self):
        entry = self._entry("> One.\n> — [Steve Jobs](/people/steve-jobs/)\n")
        self.assertEqual(entry.quotes.count(), 1)
        entry.body = "> Two.\n> — [Steve Jobs](/people/steve-jobs/)\n"
        entry.save()
        self.assertEqual(entry.quotes.count(), 1)
        self.assertEqual(entry.quotes.get().text, 'Two.')

    def test_removing_quote_from_body_deletes_it(self):
        entry = self._entry("> One.\n> — [Steve Jobs](/people/steve-jobs/)\n")
        entry.body = "No quotes here."
        entry.save()
        self.assertEqual(entry.quotes.count(), 0)

    def test_source_url_persisted(self):
        entry = self._entry(
            "> Ship.\n> — [Steve Jobs](/people/steve-jobs/) · [src](https://e.com/x)\n"
        )
        self.assertEqual(entry.quotes.get().source_url, 'https://e.com/x')


class QuoteVisibilityTests(TestCase):
    """The /quotes/ page hides quotes from unpublished entries for visitors."""

    def setUp(self):
        self.person = Person.objects.create(name='Steve Jobs', slug='steve-jobs')

    def test_draft_quotes_hidden_from_anonymous(self):
        Entry.objects.create(
            title='Draft', slug='draft', is_published=False,
            body="> Secret.\n> — [Steve Jobs](/people/steve-jobs/)\n",
        )
        response = self.client.get('/quotes/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Secret.')

    def test_published_quotes_shown(self):
        Entry.objects.create(
            title='Live', slug='live', is_published=True,
            body="> Public.\n> — [Steve Jobs](/people/steve-jobs/)\n",
        )
        response = self.client.get('/quotes/')
        self.assertContains(response, 'Public.')
