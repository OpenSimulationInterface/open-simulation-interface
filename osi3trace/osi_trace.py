"""
Module to handle and manage OSI trace files.
"""

import lzma
import struct

from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_sensorviewconfiguration_pb2 import SensorViewConfiguration
from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_hostvehicledata_pb2 import HostVehicleData
from osi3.osi_sensordata_pb2 import SensorData
from osi3.osi_trafficcommand_pb2 import TrafficCommand
from osi3.osi_trafficcommandupdate_pb2 import TrafficCommandUpdate
from osi3.osi_trafficupdate_pb2 import TrafficUpdate
from osi3.osi_motionrequest_pb2 import MotionRequest
from osi3.osi_streamingupdate_pb2 import StreamingUpdate


MESSAGES_TYPE = {
    "SensorView": SensorView,
    "SensorViewConfiguration": SensorViewConfiguration,
    "GroundTruth": GroundTruth,
    "HostVehicleData": HostVehicleData,
    "SensorData": SensorData,
    "TrafficCommand": TrafficCommand,
    "TrafficCommandUpdate": TrafficCommandUpdate,
    "TrafficUpdate": TrafficUpdate,
    "MotionRequest": MotionRequest,
    "StreamingUpdate": StreamingUpdate,
}


class OSITrace:
    """This class can import and decode OSI trace files."""

    @staticmethod
    def map_message_type(type_name):
        """Map the type name to the protobuf message type."""
        return MESSAGES_TYPE[type_name]

    @staticmethod
    def message_types():
        """Message types that OSITrace supports."""
        return list(MESSAGES_TYPE.keys())

    def __init__(self, path=None, type_name="SensorView", cache_messages=False):
        self.type = self.map_message_type(type_name)
        self.file = None
        self.current_index = None
        self.message_offsets = None
        self.read_complete = False
        self.message_cache = {} if cache_messages else None
        self._header_length = 4
        if path:
            self.from_file(path, type_name, cache_messages)

    def from_file(self, path, type_name="SensorView", cache_messages=False):
        """Import a trace from a file"""
        self.type = self.map_message_type(type_name)

        if path.lower().endswith((".lzma", ".xz")):
            self.file = lzma.open(path, "rb")
        else:
            self.file = open(path, "rb")

        self.read_complete = False
        self.current_index = 0
        self.message_offsets = [0]
        self.message_cache = {} if cache_messages else None

    def retrieve_offsets(self, limit=None):
        """Retrieve the offsets of the messages from the file."""
        if not self.read_complete:
            self.current_index = len(self.message_offsets) - 1
            self.file.seek(self.message_offsets[-1], 0)
        while not self.read_complete and (
            not limit or len(self.message_offsets) <= limit
        ):
            self.retrieve_message(skip=True)
        return self.message_offsets

    def retrieve_message(self, index=None, skip=False):
        """Retrieve the next message from the file at the current position or given index, or skip it if skip is true."""
        if index is not None:
            self.current_index = index
            self.file.seek(self.message_offsets[index], 0)
        if self.message_cache is not None and self.current_index in self.message_cache:
            message = self.message_cache[self.current_index]
            self.current_index += 1
            if self.current_index == len(self.message_offsets):
                self.file.seek(0, 2)
            else:
                self.file.seek(self.message_offsets[self.current_index], 0)
            if skip:
                return self.message_offsets[self.current_index]
            else:
                return message
        start = self.file.tell()
        header = self.file.read(self._header_length)
        if len(header) < self._header_length:
            if start == self.message_offsets[-1]:
                self.message_offsets.pop()
                self.read_complete = True
            self.file.seek(start, 0)
            return None
        message_length = struct.unpack("<L", header)[0]
        if skip:
            new_pos = self.file.seek(message_length, 1)
            if new_pos - start < message_length + self._header_length:
                if start == self.message_offsets[-1]:
                    self.message_offsets.pop()
                    self.read_complete = True
                self.file.seek(start, 0)
                return None
            self.current_index += 1
            if start == self.message_offsets[-1]:
                self.message_offsets.append(new_pos)
            return new_pos
        message_data = self.file.read(message_length)
        if len(message_data) < message_length:
            if start == self.message_offsets[-1]:
                self.message_offsets.pop()
                self.read_complete = True
            self.file.seek(start, 0)
            return None
        self.current_index += 1
        message = self.type()
        message.ParseFromString(message_data)
        if start == self.message_offsets[-1]:
            if self.message_cache is not None:
                self.message_cache[len(self.message_offsets) - 1] = message
            self.message_offsets.append(self.file.tell())
        return message

    def restart(self, index=None):
        """Restart the reading of the file from the beginning or from a given index."""
        self.current_index = index if index else 0
        self.file.seek(self.message_offsets[self.current_index], 0)

    def __iter__(self):
        while message := self.retrieve_message():
            yield message

    def get_message_by_index(self, index):
        """
        Get a message by its index.
        """
        if index >= len(self.message_offsets):
            self.retrieve_offsets(index)
        if self.message_cache is not None and index in self.message_cache:
            return self.message_cache[index]
        return self.retrieve_message(index=index)

    def get_messages(self):
        """
        Yield an iterator over all messages in the file.
        """
        return self.get_messages_in_index_range(0, None)

    def get_messages_in_index_range(self, begin, end):
        """
        Yield an iterator over messages of indexes between begin and end included.
        """
        if begin >= len(self.message_offsets):
            self.retrieve_offsets(begin)
        self.restart(begin)
        current = begin
        while end is None or current < end:
            if self.message_cache is not None and current in self.message_cache:
                yield self.message_cache[current]
            else:
                message = self.retrieve_message()
                if message is None:
                    break
                yield message
            current += 1

    def close(self):
        if self.file:
            self.file.close()
        self.file = None
        self.current_index = None
        self.message_cache = None
        self.message_offsets = None
        self.read_complete = False
        self.read_limit = None
        self.type = None
