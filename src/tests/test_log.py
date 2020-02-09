import unittest
import sys 
from utils import captured_output
sys.path.append("/app/code/")
from Log import Log

class TestLog(unittest.TestCase):
    def testSetTag(self): 
        l = Log(TAG="test_tag", display_output=True)
        with captured_output() as (out, err):
            l.setTag("test_tag_2")
            l.v("{} ~ {}")
        expected_msg = "test_tag_2 > {} ~ {}"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

    def test_i(self):
        l = Log(TAG="test_tag", display_output=True)
        with captured_output() as (out, err):
            l.i("test_msg") 
        expected_msg = "test_tag ~~~ TEST_MSG ~~~"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

    def test_v(self):
        l = Log(TAG="test_tag", display_output=True)
        with captured_output() as (out, err):
            l.v("test_msg")  
        expected_msg = "test_tag > test_msg"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

    def test_e(self): 
        l = Log(TAG="test_tag", display_output=True)
        with captured_output() as (out, err):
            l.e("test_msg") 
        expected_msg = "test_tag > !!! test_msg !!!"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

if __name__ == '__main__':
    unittest.main()
