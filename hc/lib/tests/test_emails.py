from smtplib import SMTPServerDisconnected
from unittest.mock import Mock, patch

from django.test import TestCase
from hc.lib.emails import EmailThread


@patch("hc.lib.emails.time.sleep")
class EmailsTestCase(TestCase):
    def test_it_retries(self, mock_time):
        mock_msg = Mock()
        mock_msg.send = Mock(side_effect=[SMTPServerDisconnected, None])

        t = EmailThread(mock_msg)
        t.run()

        self.assertEqual(mock_msg.send.call_count, 2)

    def test_it_limits_retries(self, mock_time):
        mock_msg = Mock()
        mock_msg.send = Mock(side_effect=SMTPServerDisconnected)

        with self.assertRaises(SMTPServerDisconnected):
            t = EmailThread(mock_msg)
            t.run()

        self.assertEqual(mock_msg.send.call_count, 3)
