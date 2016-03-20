from tags_counter.tasks import extract_tags
import unittest


class TestTagsExtractor(unittest.TestCase):
    def test_empty_input(self):
        resp = extract_tags('')
        self.assertDictEqual(resp, {})

    def test_without_tags(self):
        resp = extract_tags('La la la bum bum')
        self.assertEqual(resp, {})

    def test_set_1(self):
        with open('./test_set_openflashcards.html') as test_set_content:
            resp = extract_tags(test_set_content.readline())
            right_answer = {
                'a': 7,
                'base': 1,
                'body': 1,
                'button': 1,
                'div': 4,
                'head': 1,
                'html': 1,
                'i': 2,
                'img': 1,
                'li': 6,
                'link': 1,
                'meta': 3,
                'nav': 1,
                'noscript': 1,
                'span': 5,
                'title': 1,
                'ul': 3,
                'script': 1
            }
            self.assertDictEqual(dict(resp), right_answer)

    def test_tags_with_numbers(self):
        resp = extract_tags('<body>tralalla <col6><md4></md4></col6>')
        self.assertDictEqual(resp, dict(body=1,col6=1, md4=1))

    def test_tags_dash(self):
        resp = extract_tags('<body> qqweqwe <h1>hello</h1> <col-md-6></col-md-6>')
        self.assertEqual(resp, {'body': 1, 'h1': 1, 'col-md-6': 1})

    def test_short_tags(self):
        resp = extract_tags('<img src="/super-porno.jpeg" width=1024 />')
        self.assertDictEqual(resp, {'img': 1})