import unittest
import requests
from unittest.mock import patch
#patch helps temp replace smt while running tests
from monitor import detect_status_change, check_service_status

class TestStatusChangeDetection(unittest.TestCase):

    def test_online_to_unreachable(self):
        result = detect_status_change("online", "unreachable")
        self.assertEqual(result, "incident")

    def test_online_to_error(self):
        result = detect_status_change("online", "error")
        self.assertEqual(result, "incident")

    def test_unreachable_to_online(self):
        result = detect_status_change("unreachable", "online")
        self.assertEqual(result, "recovery")

    def test_online_to_online(self):
        result = detect_status_change("online", "online")
        #self.assertEqual(result, None)
        self.assertIsNone(result)

    def test_error_to_unreachable(self):
        result = detect_status_change("error", "unreachable")
        self.assertEqual(result, "change")



class TestServiceStatus(unittest.TestCase):

    @patch("monitor.requests.get")
    def test_http_200_is_online(self, mock_get):
        #fake response
        mock_get.return_value.status_code = 200
        mock_get.return_value.elapsed.total_seconds.return_value = 0.25

        #run function
        result = check_service_status("https://testurl.com")
        self.assertEqual(result["status"], "online")
        self.assertEqual(result["http_status_code"], 200)
        mock_get.assert_called_once_with(
            "https://testurl.com",
        timeout=5 #checking the timeout part works as well
        )

    #http500
    @patch("monitor.requests.get")
    def test_http_500_is_error(self, mock_get):
        #make fake responses for the test, run the function, assert results

        #fake response
        mock_get.return_value.status_code = 500
        mock_get.return_value.elapsed.total_seconds.return_value = 0.67 #hehe:P

        result = check_service_status("https://testurl.com")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["http_status_code"], 500)

    #for unreachable service, not response from requests.get()
    @patch("monitor.requests.get")
    def test_request_failure_is_unreachable(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException

        result = check_service_status("https://testurl.com")
        self.assertEqual(result["status"], "unreachable")
        self.assertIsNone(result["http_status_code"])
        self.assertIsNone(result["response_time"])
        mock_get.assert_called_once_with(
            "https://testurl.com",
            timeout=5
        )


    
            
if __name__ == "__main__":
    unittest.main()