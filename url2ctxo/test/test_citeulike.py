import unittest
from mock import Mock
import citeulike

class CiteulikeTest(unittest.TestCase):

    def testUrl2Citation(self):
        fPopen = Mock()
        fPopen.return_value = fPopen
        fake_output = """
            issn -> 5555-5555
            title -> Do you feel lucky, punk?
            fiftyfourleven
            """
        fOutput = Mock()
        fOutput.return_value = fake_output, None
        fPopen.communicate = fOutput

        citeulike.Popen = fPopen
        c = citeulike.url2citation('/a/fake/path', 'http://example.com')
        self.assertEqual(c.issn, '5555-5555')
        self.assertEqual(c.title, 'Do you feel lucky, punk?')
        
    def testInit(self):
        metadata = { 'issn': '0000-0019', 'title': 'Foo!' }
        c = citeulike.Citation(metadata)
        self.assertEqual(c.issn, '0000-0019')
        self.assertEqual(c.title, 'Foo!')

    def testAuthors(self):
        metadata = { 'authors': '{Au Yoris YA {Au, Yoris A.}} {Kauffman Robert RJ {Kauffman, Robert J.}}' }
        c = citeulike.Citation(metadata)
        author_list = c.authors
        self.assertEqual(author_list, ['Au, Yoris A.','Kauffman, Robert J.'])

if __name__ == '__main__':
    unittest.main()
