import unittest
from request_validator import Validator
from solution import JobsExecutor


class TestRequests(unittest.TestCase):
    def test_Validator(self):
        data_test_1 = {
            "jobs": [
                {
                    "name": "foo",
                    "commands": [
                        "python -c \"print('This is foo')\"",
                        "python -c \"import time; time.sleep(2)\""
                    ],
                    "result_directory": "/tmp/foo"
                },
                {
                    "name": "bar",
                    "commands": [
                        "python -c \"print('This is bar')\"",
                        "python -c \"import time; time.sleep(1)\""
                    ],
                    "result_directory": "/tmp/bar"
                },
                {
                    "name": "baz",
                    "commands": [
                        "python -c exit(42)"
                    ],
                    "result_directory": "/tmp/baz"
                }
            ]
        }

        data_test_2 = {
            "job": [
                {
                    "name": "foo",
                    "commands": [
                        "python -c \"print('This is foo')\"",
                        "python -c \"import time; time.sleep(2)\""
                    ],
                    "result_directory": "/tmp/foo"
                },
                {
                    "name": "bar",
                    "commands": [
                        "python -c \"print('This is bar')\"",
                        "python -c \"import time; time.sleep(1)\""
                    ],
                    "result_directory": "/tmp/bar"
                },
                {
                    "name": "baz",
                    "commands": [
                        "python -c exit(42)"
                    ],
                    "result_directory": "/tmp/baz"
                }
            ]
        }

        v1 = Validator(data_test_1)
        is_valid_1 = v1.is_valid_data()
        res_1 = v1.get_res()
        res_1_expected = {}

        v2 = Validator(data_test_2)
        is_valid_2 = v2.is_valid_data()
        res_2 = v2.get_res()
        res_2_expected = {
            'results': {'overall': 'FAIL'},
            'message': 'Unknown field "job"'
        }

        self.assertEqual(is_valid_1, True)
        self.assertEqual(res_1, res_1_expected)

        self.assertEqual(is_valid_2, False)
        self.assertEqual(res_2, res_2_expected)

    def test_JobsExecutor(self):
        data_test = {
            "jobs": [
                {
                    "name": "foo",
                    "commands": [
                        # FAIL
                        "pytho -c \"print('This is foo')\"",
                        "python -c \"import time; time.sleep(2)\""
                    ],
                    "result_directory": "/tmp/foo"
                },
                {
                    "name": "correct_foo",
                    "commands": [
                        "python -c \"print('This is foo')\"",
                        "python -c \"import time; time.sleep(2)\""
                    ],
                    "result_directory": "/tmp/foo"
                },
                {
                    "name": "bar",
                    "commands": [
                        "python -c \"print('This is bar')\"",
                        "python -c \"import time; time.sleep(1)\""
                    ],
                    "result_directory": "/tmp/bar"
                },
                {
                    "name": "baz",
                    "commands": [
                        "python -c exit(42)"
                    ],
                    "result_directory": "/tmp/baz"
                }
            ]
        }

        je = JobsExecutor(data_test)
        je.start_execution()
        res = {}
        res['results'] = je.get_results()
        res_expected = {
            "results": {
                "foo": "FAIL",
                "bar": "OK",
                "baz": "FAIL",
                "correct_foo": "OK"
            }
        }

        self.assertEqual(res, res_expected)


if __name__ == '__main__':
    unittest.main()
