"""Module for password enter frame classes."""
from enum import Enum
from .frame import FrameBase
from .exception import PyVLXException
from .const import Command
from .string_helper import string_to_bytes, bytes_to_string


class FramePasswordEnterRequest(FrameBase):
    """Frame for sending password enter request."""

    MAX_SIZE = 32

    def __init__(self, password=None):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_ENTER_REQ)
        self.password = password

    def get_payload(self):
        """Return Payload."""
        if self.password is None:
            raise PyVLXException("password is none")
        if len(self.password) > self.MAX_SIZE:
            raise PyVLXException("password is too long")
        return string_to_bytes(self.password, self.MAX_SIZE)

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.password = bytes_to_string(payload)

    def __str__(self):
        """Return human readable string."""
        return '<FramePasswordEnterRequest password=\'{}******\'/>'.format(self.password[:2])


class PasswortEnterConfirmationStatus(Enum):
    """Enum class for status of password enter confirmation."""

    SUCCESSFUL = 0
    FAILED = 1


class FramePasswordEnterConfirmation(FrameBase):
    """Frame for confirmation for sent password."""

    def __init__(self, status=PasswortEnterConfirmationStatus.SUCCESSFUL):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_ENTER_CFM)
        self.status = status

    def get_payload(self):
        """Return Payload."""
        return bytes([self.status.value])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.status = PasswortEnterConfirmationStatus(payload[0])

    def __str__(self):
        """Return human readable string."""
        return '<FramePasswordEnterConfirmation status=\'{}\'/>'.format(self.status)