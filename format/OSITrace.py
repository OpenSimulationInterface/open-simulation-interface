# Copyright 2019 -- 2024 BMW AG
# SPDX-License-Identifier: MPL-2.0
"""
Module to handle and manage OSI trace files.
"""
from collections import deque
from tqdm import tqdm
import time
import lzma
import struct
import warnings

warnings.simplefilter("default")

from osi3.osi_sensorview_pb2 import SensorView
from osi3.osi_groundtruth_pb2 import GroundTruth
from osi3.osi_sensordata_pb2 import SensorData

SEPARATOR = b"$$__$$"
SEPARATOR_LENGTH = len(SEPARATOR)


def get_size_from_file_stream(file_object):
    """
    Return a file size from a file stream given in parameters
    """
    current_position = file_object.tell()
    file_object.seek(0, 2)
    size = file_object.tell()
    file_object.seek(current_position)
    return size


MESSAGES_TYPE = {
    "SensorView": SensorView,
    "GroundTruth": GroundTruth,
    "SensorData": SensorData,
}


class OSITrace:
    """This class wrap OSI data. It can import and decode OSI trace files."""

    def __init__(self, buffer_size=0, show_progress=True, type_name="SensorView"):
        self.path = None
        self.trace_file = None
        self.message_offsets = None
        self.buffer_size = buffer_size
        self._int_length = len(struct.pack("<L", 0))
        self.type_name = type_name
        self.message_cache = {}
        self.timestep_count = 0
        self.show_progress = show_progress
        self.retrieved_trace_size = 0

    def from_file(self, path, type_name="SensorView", max_index=-1, format_type=None):
        """Import a trace from a file"""
        self.path = path
        if self.path.lower().endswith((".lzma", ".xz")):
            self.trace_file = lzma.open(path, "rb")
        else:
            self.trace_file = open(path, "rb")

        self.type_name = type_name

        if self.path.lower().endswith(".txt"):
            self.timestep_count = self.retrieve_message_offsets(max_index)
        else:
            self.timestep_count = self.retrieve_message()

    def retrieve_message_offsets(self, max_index):
        """
        Retrieve the offsets of all the messages of the txt trace and store them
        in the `message_offsets` attribute of the object

        It returns the number of discovered timesteps
        """
        trace_size = get_size_from_file_stream(self.trace_file)

        if max_index == -1:
            max_index = float("inf")

        # For $$__$$ separated trace files the buffersize needs to be greater than zero
        if self.buffer_size == 0:
            self.buffer_size = 1000000  # Make it backwards compatible

        if self.show_progress:
            progress_bar = tqdm(total=trace_size)
            print(
                "Retrieving message offsets in txt trace file until "
                + str(trace_size)
                + " ..."
            )
        else:
            progress_bar = None

        buffer_deque = deque(maxlen=2)

        self.message_offsets = [0]
        eof = False

        if self.show_progress:
            start_time = time.time()

        self.trace_file.seek(0)

        while not eof and len(self.message_offsets) <= max_index:
            found = -1  # SEP offset in buffer
            buffer_deque.clear()

            while found == -1 and not eof:
                new_read = self.trace_file.read(self.buffer_size)
                buffer_deque.append(new_read)
                buffer = b"".join(buffer_deque)
                found = buffer.find(SEPARATOR)
                eof = len(new_read) != self.buffer_size

            buffer_offset = self.trace_file.tell() - len(buffer)
            message_offset = found + buffer_offset + SEPARATOR_LENGTH
            self.message_offsets.append(message_offset)
            progress_bar.update(message_offset)
            last_offset = message_offset
            self.trace_file.seek(message_offset)

            while eof and found != -1:
                buffer = buffer[found + SEPARATOR_LENGTH :]
                found = buffer.find(SEPARATOR)

                buffer_offset = trace_size - len(buffer)

                message_offset = found + buffer_offset + SEPARATOR_LENGTH

                if message_offset >= trace_size:
                    break
                self.message_offsets.append(message_offset)
                progress_bar.update(message_offset - last_offset)
                last_offset = message_offset

        if eof:
            self.retrieved_trace_size = trace_size
        else:
            self.retrieved_trace_size = self.message_offsets[-1]
            self.message_offsets.pop()

        if self.show_progress:
            progress_bar.close()
            print(
                len(self.message_offsets),
                "messages has been discovered in",
                time.time() - start_time,
                "s",
            )

        return len(self.message_offsets)

    def retrieve_message(self):
        """
        Retrieve the offsets of all the messages of the osi trace and store them
        in the `message_offsets` attribute of the object

        It returns the number of discovered timesteps
        """
        trace_size = get_size_from_file_stream(self.trace_file)

        if self.show_progress:
            progress_bar = tqdm(total=trace_size)
            print(
                "Retrieving messages in osi trace file until "
                + str(trace_size)
                + " ..."
            )
        else:
            progress_bar = None

        eof = False

        if self.show_progress:
            start_time = time.time()

        self.trace_file.seek(0)

        self.message_offsets = [0]
        message_offset = 0
        last_offset = 0
        message_length = 0
        counter = 0  # Counter is needed to enable correct buffer parsing of serialized messages

        # Check if user decided to use buffer
        if self.buffer_size != 0 and type(self.buffer_size) == int:
            # Run while the end of file is not reached
            while not eof and message_offset < trace_size:
                serialized_message = self.trace_file.read(self.buffer_size)
                self.trace_file.seek(self.message_offsets[-1])

                while not eof:
                    # Unpack the message size relative to the current buffer
                    message_length = struct.unpack(
                        "<L",
                        serialized_message[
                            message_offset
                            - counter * self.buffer_size : self._int_length
                            + message_offset
                            - counter * self.buffer_size
                        ],
                    )[0]

                    # Get the message offset of the next message
                    message_offset += message_length + self._int_length
                    self.message_offsets.append(message_offset)
                    progress_bar.update(message_offset - last_offset)
                    last_offset = message_offset
                    self.trace_file.seek(message_offset)
                    eof = self.trace_file.tell() > self.buffer_size * (counter + 1)

                    # Check if reached end of file
                    if self.trace_file.tell() == trace_size:
                        self.retrieved_trace_size = self.message_offsets[-1]
                        self.message_offsets.pop()  # Remove the last element since after that there is no message coming
                        break

                while eof:
                    # Counter increment and cursor placement update. The cursor is set absolute in the file.
                    if message_offset >= len(serialized_message):
                        progress_bar.update(message_offset - last_offset)
                        last_offset = message_offset
                        counter += 1
                        self.trace_file.seek(counter * self.buffer_size)
                        eof = False

        else:
            serialized_message = self.trace_file.read()
            while message_offset < trace_size:
                message_length = struct.unpack(
                    "<L",
                    serialized_message[
                        message_offset : self._int_length + message_offset
                    ],
                )[0]
                message_offset += message_length + self._int_length
                self.message_offsets.append(message_offset)
                progress_bar.update(message_offset - last_offset)
                last_offset = message_offset

            self.retrieved_trace_size = self.message_offsets[-1]
            self.message_offsets.pop()

        if self.show_progress:
            progress_bar.close()
            print(
                len(self.message_offsets),
                "messages has been discovered in",
                time.time() - start_time,
                "s",
            )

        return len(self.message_offsets)

    def get_message_by_index(self, index):
        """
        Get a message by its index. Try first to get it from the cache made
        by the method ``cache_messages_in_index_range``.
        """
        message = self.message_cache.get(index, None)

        if message is not None:
            return message

        return next(self.get_messages_in_index_range(index, index + 1))

    def get_messages(self):
        return self.get_messages_in_index_range(0, len(self.message_offsets))

    def get_messages_in_index_range(self, begin, end):
        """
        Yield an iterator over messages of indexes between begin and end included.
        """

        self.trace_file.seek(self.message_offsets[begin])
        abs_first_offset = self.message_offsets[begin]
        abs_last_offset = (
            self.message_offsets[end]
            if end < len(self.message_offsets)
            else self.retrieved_trace_size
        )

        rel_message_offsets = [
            abs_message_offset - abs_first_offset
            for abs_message_offset in self.message_offsets[begin:end]
        ]

        if self.path.lower().endswith((".txt")):
            message_sequence_len = abs_last_offset - abs_first_offset - SEPARATOR_LENGTH
            serialized_messages_extract = self.trace_file.read(message_sequence_len)

            pbar = tqdm(rel_message_offsets)
            for rel_index, rel_message_offset in enumerate(pbar):
                pbar.set_description(
                    f"Processing index {rel_index} with offset {rel_message_offset}"
                )
                rel_begin = rel_message_offset
                rel_end = (
                    rel_message_offsets[rel_index + 1] - SEPARATOR_LENGTH
                    if rel_index + 1 < len(rel_message_offsets)
                    else message_sequence_len
                )

                message = MESSAGES_TYPE[self.type_name]()
                serialized_message = serialized_messages_extract[rel_begin:rel_end]
                message.ParseFromString(serialized_message)
                yield message

        elif self.path.lower().endswith((".osi")):
            message_sequence_len = abs_last_offset - abs_first_offset
            serialized_messages_extract = self.trace_file.read(message_sequence_len)
            message_length = 0
            i = 0
            while i < len(serialized_messages_extract):
                message = MESSAGES_TYPE[self.type_name]()
                message_length = struct.unpack(
                    "<L", serialized_messages_extract[i : self._int_length + i]
                )[0]
                message.ParseFromString(
                    serialized_messages_extract[
                        i + self._int_length : i + self._int_length + message_length
                    ]
                )
                i += message_length + self._int_length
                yield message

        else:
            raise Exception(
                f"The defined file format {self.path.split('/')[-1]} does not exist."
            )

    def cache_messages_in_index_range(self, begin, end):
        """
        Put all messages from index begin to index end in the cache. Then the
        method ``get_message_by_index`` can access to it in a faster way.

        Using this method again clear the last cache and replace it with a new
        one.
        """
        if self.show_progress:
            print("\nCaching ...")
        self.message_cache = {
            index + begin: message
            for index, message in enumerate(
                self.get_messages_in_index_range(begin, end)
            )
        }

        if self.show_progress:
            print("Caching done!")

    def make_readable(self, name, interval=None, index=None):
        self.trace_file.seek(0)
        serialized_message = self.trace_file.read()
        message_length = len(serialized_message)

        if message_length > 1000000000:
            # Throw a warning if trace file is bigger than 1GB
            gb_size_input = round(message_length / 1000000000, 2)
            gb_size_output = round(3.307692308 * message_length / 1000000000, 2)
            warnings.warn(
                f"The trace file you are trying to make readable has the size {gb_size_input}GB. This will generate a readable file with the size {gb_size_output}GB. Make sure you have enough disc space and memory to read the file with your text editor.",
                ResourceWarning,
            )

        with open(name, "a") as f:
            if interval is None and index is None:
                for i in self.get_messages():
                    f.write(str(i))

            if interval is not None and index is None:
                if (
                    type(interval) == tuple
                    and len(interval) == 2
                    and interval[0] < interval[1]
                ):
                    for i in self.get_messages_in_index_range(interval[0], interval[1]):
                        f.write(str(i))
                else:
                    raise Exception(
                        "Argument 'interval' needs to be a tuple of length 2! The first number must be smaller then the second."
                    )

            if interval is None and index is not None:
                if type(index) == int:
                    f.write(str(self.get_message_by_index(0)))
                else:
                    raise Exception("Argument 'index' needs to be of type 'int'")

            if interval is not None and index is not None:
                raise Exception("Arguments 'index' and 'interval' can not be set both")
