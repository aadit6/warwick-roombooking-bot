import unittest
from unittest.mock import patch, MagicMock, Mock
import smtplib
import os
import sys
import requests
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load real environment variables
load_dotenv()

from check_wrb2526 import check_page, send_email, URL, CHECK_STRING


class TestWRBChecker(unittest.TestCase):
    """Test suite for the Warwick Room Booking checker bot."""

    def setUp(self):
        """Set up test environment."""
        # Use real environment variables from .env file
        self.real_email_user = os.getenv("EMAIL_USER")
        self.real_email_pass = os.getenv("EMAIL_PASS")
        self.real_to_email = os.getenv("TO_EMAIL")
        
        # Ensure we have real credentials for testing
        if not all([self.real_email_user, self.real_email_pass, self.real_to_email]):
            self.skipTest("Real email credentials not configured in .env file")

    def tearDown(self):
        """Clean up after tests."""
        pass

    @patch('check_wrb2526.smtplib.SMTP_SSL')
    def test_send_email_success(self, mock_smtp_ssl):
        """Test that email sending works correctly."""
        # Mock SMTP_SSL server
        mock_server = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server
        
        # Call send_email
        send_email("test status")
        
        # Verify SMTP_SSL was called correctly (port 465)
        mock_smtp_ssl.assert_called_once_with("smtp.gmail.com", 465, timeout=30)
        # No starttls() call for SMTP_SSL (it's already encrypted)
        mock_server.login.assert_called_once_with(self.real_email_user, self.real_email_pass)
        mock_server.send_message.assert_called_once()

    @patch('check_wrb2526.smtplib.SMTP_SSL')
    def test_send_email_smtp_error(self, mock_smtp_ssl):
        """Test email sending handles SMTP errors gracefully."""
        # Mock SMTP_SSL to raise an exception
        mock_smtp_ssl.side_effect = smtplib.SMTPException("SMTP Error")
        
        # Should raise the exception (we might want to handle this in the actual code)
        with self.assertRaises(smtplib.SMTPException):
            send_email("test status")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_still_unavailable(self, mock_send_email, mock_get):
        """Test when page still shows 'Application Unavailable'."""
        # Mock response with unavailable message
        mock_response = Mock()
        mock_response.text = f"Some text {CHECK_STRING} more text"
        mock_response.url = URL
        mock_get.return_value = mock_response

        with patch('builtins.print') as mock_print:
            check_page()
            mock_print.assert_called_once_with("Still unavailable.")
            mock_send_email.assert_not_called()

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_redirected_to_login(self, mock_send_email, mock_get):
        """Test when page redirects to login (system is live)."""
        # Mock response with login redirect
        mock_response = Mock()
        mock_response.text = "Login page content"
        mock_response.url = "https://abs.warwick.ac.uk/Login.aspx?ReturnUrl=/WRB2526/"
        mock_get.return_value = mock_response

        check_page()
        mock_send_email.assert_called_once_with("Redirected to login (system live)")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_return_url_in_url(self, mock_send_email, mock_get):
        """Test when ReturnUrl is in the URL (another login scenario)."""
        # Mock response with ReturnUrl in URL
        mock_response = Mock()
        mock_response.text = "Some content"
        mock_response.url = "https://abs.warwick.ac.uk/some/path?ReturnUrl=/WRB2526/"
        mock_get.return_value = mock_response

        check_page()
        mock_send_email.assert_called_once_with("Redirected to login (system live)")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_booking_form_detected_wrb(self, mock_send_email, mock_get):
        """Test when the booking form is detected (Web Room Booking System 2025/26)."""
        # Mock response with booking form
        mock_response = Mock()
        mock_response.text = "Welcome to Web Room Booking System 2025/26"
        mock_response.url = URL
        mock_get.return_value = mock_response

        check_page()
        mock_send_email.assert_called_once_with("Booking form detected")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_booking_form_detected_preferred_start(self, mock_send_email, mock_get):
        """Test when the booking form is detected (Preferred Start text)."""
        # Mock response with booking form (no year mentioned)
        mock_response = Mock()
        mock_response.text = "Please select your Preferred Start date"
        mock_response.url = URL
        mock_get.return_value = mock_response

        check_page()
        mock_send_email.assert_called_once_with("Booking form detected")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_booking_form_preferred_start_2425(self, mock_send_email, mock_get):
        """Test when Preferred Start is found but with wrong year (2024/25)."""
        # Mock response with wrong year
        mock_response = Mock()
        mock_response.text = "Web Room Booking System 2024/25 - Please select your Preferred Start date"
        mock_response.url = URL
        mock_get.return_value = mock_response

        with patch('builtins.print') as mock_print:
            check_page()
            mock_print.assert_called_once_with("Page changed, but not sure what it is. Check manually.")
            mock_send_email.assert_called_once_with("UNEXPECTED CHANGE - Page changed but not recognized as booking system. Manual check required.")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_booking_form_preferred_start_2526(self, mock_send_email, mock_get):
        """Test when Preferred Start is found with correct year (2025/26)."""
        # Mock response with correct year
        mock_response = Mock()
        mock_response.text = "Room Booking 2025/26 - Please select your Preferred Start date"
        mock_response.url = URL
        mock_get.return_value = mock_response

        check_page()
        mock_send_email.assert_called_once_with("Booking form detected")

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_unknown_change(self, mock_send_email, mock_get):
        """Test when page changes but doesn't match expected patterns."""
        # Mock response with unknown content
        mock_response = Mock()
        mock_response.text = "Some completely different content"
        mock_response.url = URL
        mock_get.return_value = mock_response

        with patch('builtins.print') as mock_print:
            check_page()
            mock_print.assert_called_once_with("Page changed, but not sure what it is. Check manually.")
            mock_send_email.assert_called_once_with("UNEXPECTED CHANGE - Page changed but not recognized as booking system. Manual check required.")

    @patch('check_wrb2526.requests.get')
    def test_check_page_request_exception(self, mock_get):
        """Test handling of request exceptions."""
        # Mock requests to raise an exception
        mock_get.side_effect = requests.RequestException("Network error")
        
        # Should raise the exception (we might want to handle this in the actual code)
        with self.assertRaises(requests.RequestException):
            check_page()

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.send_email')
    def test_check_page_redirects_allowed(self, mock_send_email, mock_get):
        """Test that redirects are properly followed."""
        mock_response = Mock()
        mock_response.text = "Login page"
        mock_response.url = "https://abs.warwick.ac.uk/Login.aspx"
        mock_get.return_value = mock_response

        check_page()
        
        # Verify requests.get was called with allow_redirects=True
        mock_get.assert_called_once_with(URL, allow_redirects=True)

    def test_constants_defined(self):
        """Test that required constants are properly defined."""
        self.assertEqual(URL, "https://abs.warwick.ac.uk/WRB2526/")
        self.assertEqual(CHECK_STRING, "Application Unavailable")

    def test_environment_variables_loaded(self):
        """Test that environment variables are properly accessed."""
        # These should be real environment variables from .env
        self.assertIsNotNone(os.getenv("EMAIL_USER"))
        self.assertIsNotNone(os.getenv("EMAIL_PASS"))
        self.assertIsNotNone(os.getenv("TO_EMAIL"))
        self.assertEqual(os.getenv("EMAIL_USER"), self.real_email_user)
        self.assertEqual(os.getenv("EMAIL_PASS"), self.real_email_pass)
        self.assertEqual(os.getenv("TO_EMAIL"), self.real_to_email)


class TestIntegration(unittest.TestCase):
    """Integration tests that test the bot with real-like scenarios."""

    def setUp(self):
        """Set up integration test environment."""
        # Use real environment variables from .env file
        self.real_email_user = os.getenv("EMAIL_USER")
        self.real_email_pass = os.getenv("EMAIL_PASS")
        self.real_to_email = os.getenv("TO_EMAIL")
        
        # Ensure we have real credentials for testing
        if not all([self.real_email_user, self.real_email_pass, self.real_to_email]):
            self.skipTest("Real email credentials not configured in .env file")

    def tearDown(self):
        """Clean up after integration tests."""
        pass

    @patch('check_wrb2526.requests.get')
    @patch('check_wrb2526.smtplib.SMTP_SSL')
    def test_full_workflow_booking_available(self, mock_smtp_ssl, mock_get):
        """Test complete workflow when booking becomes available."""
        # Mock HTTP response indicating booking is available
        mock_response = Mock()
        mock_response.text = "Web Room Booking System 2025/26 - Please select your preferred dates"
        mock_response.url = URL
        mock_get.return_value = mock_response

        # Mock SMTP_SSL
        mock_server = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_server

        # Run the check
        check_page()

        # Verify HTTP request was made
        mock_get.assert_called_once_with(URL, allow_redirects=True)
        
        # Verify email was sent with SSL on port 465
        mock_smtp_ssl.assert_called_once_with("smtp.gmail.com", 465, timeout=30)
        # No starttls() call for SMTP_SSL (it's already encrypted)
        mock_server.login.assert_called_once_with(self.real_email_user, self.real_email_pass)
        mock_server.send_message.assert_called_once()


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2) 