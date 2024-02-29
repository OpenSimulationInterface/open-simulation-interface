"""
Module to handle and manage OSI trace files.
"""
import lzma
import struct

from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_sensordata_pb2 import SensorData


MESSAGES_TYPE = {
    "SensorView": SensorView,
    "GroundTruth": GroundTruth,
    "SensorData": SensorData,
}


class OSITrace:
    """This class can import and decode OSI trace files."""

    @staticmethod
    def map_message_type(type_name):
        """Map the type name to the protobuf message type."""
        return MESSAGES_TYPE[type_name]

    def __init__(self, path=None, type_name="SensorView"):
        self.type = self.map_message_type(type_name)
        self.file = None
        self.message_offsets = None
        self.read_complete = False
        self.read_limit = None
        self._header_length = 4
        if path:
            self.from_file(path, type_name)

    def from_file(self, path, type_name="SensorView"):
        """Import a trace from a file"""
        self.type = self.map_message_type(type_name)

        if path.lower().endswith((".lzma", ".xz")):
            self.file = lzma.open(path, "rb")
        else:
            self.file = open(path, "rb")

        self.read_complete = False
        self.read_limit = 0
        self.message_offsets = [0]

    def retrieve_offsets(self, limit=None):
        """Retrieve the offsets of the messages from the file."""
        if not self.read_complete:
            self.file.seek(self.read_limit, 0)
        while not self.read_complete and not limit or len(self.message_offsets) < limit:
            self.retrieve_message(skip=True)
        return self.message_offsets

    def read_message(self, offset=None, skip=False):
        """Read a message from the file at the given offset."""
        if offset:
            self.file.seek(offset, 0)
        message = self.type()
        header = self.file.read(self._header_length)
        if len(header) < self._header_length:
            return None
        message_length = struct.unpack("<L", header)[0]
        if skip:
            self.file.seek(message_length, 1)
            return self.file.tell()
        message_data = self.file.read(message_length)
        if len(message_data) < message_length:
            return None
        message.ParseFromString(message_data)
        return message

    def retrieve_message(self, skip=False):
        """Retrieve the next message from the file, or skip it if skip is true."""
        result = self.read_message(skip=skip)
        if result is None:
            self.message_offsets.pop()
            self.read_complete = True
        if skip:
            self.read_limit = result
            self.message_offsets.append(result)
        else:
            self.read_limit = self.file.tell()
            self.message_offsets.append(self.read_limit)
        return result

    def __iter__(self):
        while message := self.retrieve_message():
            yield message

    def get_message_by_index(self, index):
        """
        Get a message by its index.
        """
        if index > len(self.message_offsets):
            self.retrieve_offsets(index)
        return self.read_message(self.message_offsets[index])

    def get_messages(self):
        return self.get_messages_in_index_range(0, None)

    def get_messages_in_index_range(self, begin, end):
        """
        Yield an iterator over messages of indexes between begin and end included.
        """
        if begin > len(self.message_offsets):
            self.retrieve_offsets(begin)
        self.file.seek(self.message_offsets[begin], 0)
        current = begin
        while end is None or current < end:
            message = (
                self.retrieve_message()
                if current >= len(self.message_offsets)
                else self.read_message()
            )
            if message is None:
                break
            yield message
            current += 1

    def close(self):
        if self.file:
            self.file.close()
        self.file = None
        self.message_offsets = None
        self.read_complete = False
        self.read_limit = None
        self.type = None
