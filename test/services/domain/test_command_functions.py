from unittest import mock

from requests.models import Response
from qwer.services.domain.command_functions import DefaultCommandFunctions
import unittest
from unittest.mock import Mock

class TestDefaultCommandFunctions(unittest.TestCase):
    def test_urlfetch_should_call_requests_get(self):
        mock_session = Mock()

        command_functions = DefaultCommandFunctions(
            session = mock_session
        )

        url = 'https://test.io/url'
        command_functions.urlfetch(url)

        mock_session.get.assert_called_with(url)
