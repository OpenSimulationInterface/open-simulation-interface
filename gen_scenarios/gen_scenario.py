from osi3.osi_sensorview_pb2 import SensorView
import struct
import argparse
import os
import random

"""
This program generates currently random scenarios with predefined message count and moving object count.

Example usage:
    python gen_scenario.py --output "movingobject" --message 10 --moving_objects 5 --random
    python gen_scenario.py --output "movingobject" --messages 100 --moving_objects 100 --random
"""


def command_line_arguments():
    """ Define and handle command line interface """

    parser = argparse.ArgumentParser(
        description="Generate OSI scenarios.", prog="gen_scenario"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Name of the output file.",
        default="output.osi",
        type=str,
    )
    parser.add_argument(
        "--messages",
        "-m",
        help="Path to the file with serialized data.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "--moving_objects",
        "-mo",
        help="Count of the movin objects.",
        default=0,
        type=int,
        required=False,
    )
    parser.add_argument(
        "--random",
        "-r",
        help="Random placement of objects into the world.",
        default=True,
        required=False,
        action="store_true",
    )

    return parser.parse_args()


def main():
    # Handling of command line arguments
    args = command_line_arguments()
    message_count = args.messages
    moving_objects_count = args.moving_objects
    use_random = args.random
    output = args.output

    moving_objects_dict = {}

    """Initialize SensorView"""
    f = open(f"sv_312_320_{moving_objects_count}_{output}.osi", "ab")
    sensorview = SensorView()

    sv_ground_truth = sensorview.global_ground_truth
    sv_ground_truth.version.version_major = 3
    sv_ground_truth.version.version_minor = 1
    sv_ground_truth.version.version_patch = 2

    sv_ground_truth.timestamp.seconds = 0
    sv_ground_truth.timestamp.nanos = 0

    # Create moving object dictionary
    for mo in range(args.moving_objects):
        moving_object = sv_ground_truth.moving_object.add()
        moving_object.id.value = mo

        moving_object.base.position.x = random.randint(0, 100) if use_random else 0.0
        moving_object.base.position.y = random.randint(0, 100) if use_random else 0.0
        moving_object.base.position.z = random.randint(0, 100) if use_random else 0.0

        # Vehicle dimension
        moving_object.base.dimension.length = 5
        moving_object.base.dimension.width = 2
        moving_object.base.dimension.height = 1

        # Classification type
        moving_object.vehicle_classification.type = 2

        # Direction
        moving_object.base.orientation.roll = 0.0
        moving_object.base.orientation.pitch = 0.0
        moving_object.base.orientation.yaw = 0.0

        # Save in dictionary
        moving_objects_dict[mo] = moving_object

    # Generate OSI messages
    for message_num in range(args.messages):

        # Increment the time by one second
        sv_ground_truth.timestamp.seconds += 1
        sv_ground_truth.timestamp.nanos = 0

        for mo_key, mo in moving_objects_dict.items():

            mo.base.position.x += 1
            mo.base.position.y = mo.base.position.y
            mo.base.position.z = mo.base.position.z

        """Serialize"""
        bytes_buffer = sensorview.SerializeToString()
        f.write(struct.pack("<L", len(bytes_buffer)))
        f.write(bytes_buffer)

    f.close()


if __name__ == "__main__":
    main()
