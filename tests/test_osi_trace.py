import os
import tempfile
import unittest

from format.OSITrace import OSITrace
from osi3.osi_sensorview_pb2 import SensorView
import struct


class TestOSITrace(unittest.TestCase):
    def test_osi_trace(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            path_output = os.path.join(tmpdirname, "output.txth")
            path_input = os.path.join(tmpdirname, "input.osi")
            create_sample(path_input)

            trace = OSITrace()
            trace.from_file(path=path_input)
            trace.make_readable(path_output, index=1)
            trace.scenario_file.close()

            self.assertTrue(os.path.exists(path_output))


def create_sample(path):
    f = open(path, "ab")
    sensorview = SensorView()

    sv_ground_truth = sensorview.global_ground_truth
    sv_ground_truth.version.version_major = 3
    sv_ground_truth.version.version_minor = 0
    sv_ground_truth.version.version_patch = 0

    sv_ground_truth.timestamp.seconds = 0
    sv_ground_truth.timestamp.nanos = 0

    moving_object = sv_ground_truth.moving_object.add()
    moving_object.id.value = 114

    # Generate 10 OSI messages for 9 seconds
    for i in range(10):
        # Increment the time
        sv_ground_truth.timestamp.seconds += 1
        sv_ground_truth.timestamp.nanos += 100000

        moving_object.vehicle_classification.type = 2

        moving_object.base.dimension.length = 5
        moving_object.base.dimension.width = 2
        moving_object.base.dimension.height = 1

        moving_object.base.position.x = 0.0 + i
        moving_object.base.position.y = 0.0
        moving_object.base.position.z = 0.0

        moving_object.base.orientation.roll = 0.0
        moving_object.base.orientation.pitch = 0.0
        moving_object.base.orientation.yaw = 0.0

        """Serialize"""
        bytes_buffer = sensorview.SerializeToString()
        f.write(struct.pack("<L", len(bytes_buffer)) + bytes_buffer)

    f.close()
