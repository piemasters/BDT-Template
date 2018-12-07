import unittest
import sys
from io import StringIO

from bdt_template import LoggingManager


class LoggingManagerTests(unittest.TestCase):

    def test_bdt_logger(self):
        sys.stdout = StringIO()

        status = 'error'
        file_id = 'LMT1 Test File'
        message = "This is a test message"
        matched_file = "text.txt"
        error = "A sample error message"

        # print message and get the result
        LoggingManager.bdt_logger(status, file_id, message, matched_file, error)
        result = sys.stdout.getvalue()

        # the new expected message format
        expected = 'ERROR: [LMT1 Test File] - This is a test message. File found: [text.txt] Error message: A sample error message\n'

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
