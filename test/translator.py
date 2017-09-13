import unittest
import requests
import deepl

paragraph_text = """This is a text with multiple paragraphs. This is still the first one.
This is the second one.

This is the third paragraph."""

paragraph_list = [
    'This is a text with multiple paragraphs. This is still the first one.',
    'This is the second one.',
    'This is the third paragraph.'
]

sentence_list = [
    'This is a text with multiple paragraphs.',
    'This is still the first one.',
    'This is the second one.',
    'This is the third paragraph.'
]


class TestOfflineMethods(unittest.TestCase):
    def test_split_paragraphs(self):
        self.assertListEqual(deepl.translator._split_paragraphs(paragraph_text), paragraph_list)

    @unittest.skip("Not yet implemented")
    def test_insert_translation(self):
        pass


class TestOnlineMethods(unittest.TestCase):
    def setUp(self):
        try:
            requests.get("https://www.deepl.com/jsonrpc")
        except ConnectionError:
            self.skipTest("Can't contact deepl API. Skipping online tests")

    def test_split_sentences(self):
        self.assertListEqual(deepl.translator._request_split_sentences(paragraph_list, "EN", ["EN"]),
                             sentence_list)

    def test_translate(self):
        self.assertListEqual(
            deepl.translator._request_translate(["This is a test"], "EN", "DE", ["EN", "DE"])["translations"],
            ["Das ist ein Test"])


if __name__ == '__main__':
    unittest.main()
