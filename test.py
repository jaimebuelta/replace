import shutil
import os
import difflib
from unittest import TestCase
from textwrap import dedent

from replace import main_replace

TEST_DIR = './test/'
INPUT = 'test_input.txt'
OUTPUT = 'test_output.txt'


class ReplaceTest(TestCase):

    def store_text_file(self, test_text, filename='test.txt'):
        path = os.path.join(TEST_DIR, filename)
        with open(path, 'w') as fp:
            fp.write(test_text)

    def get_text_file(self, filename='test.txt'):
        path = os.path.join(TEST_DIR, filename)
        with open(path) as fp:
            data = fp.read()
        return data

    def trim(self, text):
        text = text.split('\n')
        # Trim first and last line
        text = text[1:-1]
        # Trim indentation
        indentation = 10000
        for line in text:
            indentation = min(len(line) - len(line.lstrip(' ')),
                              indentation)

        text = [line[indentation:] for line in text]
        text = '\n'.join(text) + '\n'

        return text

    def store_input(self, input_text):
        input_text = self.trim(input_text)
        with open(INPUT, 'w') as fp:
            fp.write(input_text)

    def store_output(self, input_text):
        input_text = self.trim(input_text)
        with open(OUTPUT, 'w') as fp:
            fp.write(input_text)

    def replace(self):
        main_replace(INPUT, OUTPUT, TEST_DIR)

    def assertText(self, text1, text2):
        if text1 != text2:
            # Print them side by side
            for line in difflib.context_diff(text1.split('\n'),
                                             text2.split('\n'),
                                             fromfile='expected',
                                             tofile='result'):
                print line
            raise AssertionError

    def setUp(self):
        self.store_input('')
        self.store_output('')
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_DIR)
        os.remove(INPUT)
        os.remove(OUTPUT)

    def test_store_and_retrieve(self):
        TEST = '''
        self.assertRaises(Error, call, param1, param2)
        '''
        self.store_text_file(TEST)
        self.assertEqual(self.get_text_file(), TEST)

    def test_basic(self):
        self.store_input('''
        self.assertRaises(Error, call, param1, param2)
        ''')
        self.store_output('''
        with self.assertRaises():
            call(param1, param2)
        ''')

        self.store_text_file('''
        something
        self.assertRaises(Error, call, param1, param2)
        something
        ''')

        self.replace()

        expected = '''
        something
        with self.assertRaises():
            call(param1, param2)
        something
        '''

        result = self.get_text_file()
        self.assertText(expected, result)
