"""
Dreampylib - version 1.0-alpha
A python library for interacting with Dreamhost's API

(c) 2009 by Laurens Simonis
See LICENSE for licencing info
"""
import os
import uuid
import logging
import requests

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
LOGGER = logging.getLogger("dreampylib")


class _RemoteCommand:
    """
    Execute arbitrary remote api calls
      Should catch arbitrary maybe non-existent function calls.
      Supports "nested" methods (e.g. examples.getStateName)
    """

    def __init__(self, name, parent, url):
        """Initialize _RemoteCommand"""
        self._name = name
        self._cmd = name.replace(".", "-")
        self._parent = parent
        self._url = url
        self._child = None

        self._status = None
        self._result = []

    def result(self):
        """Return the result of the command"""
        if self._child:
            return self._child.result()
        return self._result

    def status(self):
        """Return the status of the command"""
        if self._child:
            return self._child.status()
        return self._status

    def __getattr__(self, name):
        """Dynamically build the command"""
        self._child = _RemoteCommand(
            "%s.%s" % (self._name, name), self._parent, self._url
        )
        return self._child

    def __call__(self, *args, **kwargs):
        """Execute the api call"""
        LOGGER.debug("Called %s(%s)", self._name, str(kwargs))

        if self._parent.is_connected():
            request = {}
            request.update(kwargs)
            request.update(self._parent._get_user_data())

            request["cmd"] = self._cmd
            request["unique_id"] = str(uuid.uuid4())
            request["format"] = "json"

            LOGGER.debug("Request: %s", request)

            response = requests.post(url=self._url, data=request).json()

            self._status = response['result']
            self._result = response['data']
            if self._status == "success":
                LOGGER.debug("Result: %s", self._result)
                return True, self._status, self._result

            LOGGER.debug('ERROR with %s: %s - %s', self._name, self._status, self._result)
            self._status = '%s: %s - %s' % (self._name, self._status, self._result)
            return False, self._status, self._result
        return []


class DreampyLib:
    """Wrapper to interact with Dreamhost's API"""
    def __init__(self, key=None, url="https://api.dreamhost.com"):
        """Initialise the connection to the dreamhost API."""
        if not key:
          key = os.getenv('API_KEY')

        self._key = key
        self._url = url
        self._last_command = None
        self._connected = False
        self._available_commands = []

        if key:
            self.connect()

    def connect(self, key=None, url=None):
        """Connect to the dreamhost API and retrive available commands"""
        if key:
            self._key = key
        if url:
            self._url = url

        self._connected = True
        self._connected, _, self._available_commands = self.api.list_accessible_cmds()

        if not self._connected:
            self._available_commands = []
            return False
        return True

    def is_connected(self):
        """Check if connected to dreamhost API"""
        return self._connected

    def result(self):
        """Return result of the command"""
        if not self._last_command:
            return []
        return self._last_command.result()

    def status(self):
        """Return status of the command"""
        if not self._last_command:
            return None
        return self._last_command.status()

    def available_commands(self):
        """List available commands and relevant info"""
        return self._available_commands

    def _get_user_data(self):
        """Privide static user information"""
        return {"key": self._key}

    def __getattr__(self, name):
        """Dynamically build command"""
        self._last_command = _RemoteCommand(name, self, self._url)
        return self._last_command

    def __dir__(self):
        """List available commands"""
        return [cmd['cmd'].replace("-", ".") for cmd in self._available_commands]
