"""
This program converts serialized osi trace files into a human readable txth file. 

Example usage:
    python3 osi2read.py -d trace.osi -o myreadableosifile
"""

from osi3trace.osi_trace import OSITrace
import argparse
import pathlib


def command_line_arguments():
    """Define and handle command line interface"""

    parser = argparse.ArgumentParser(
        description="Convert a serialized osi trace file to a readable txth output.",
        prog="osi2read",
    )
    parser.add_argument(
        "--data",
        "-d",
        help="Path to the file with serialized data.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--type",
        "-t",
        help="Name of the type used to serialize data.",
        choices=OSITrace.message_types(),
        default="SensorView",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output name of the file.",
        type=str,
        required=False,
    )

    return parser.parse_args()


def main():
    # Handling of command line arguments
    args = command_line_arguments()

    # Initialize the OSI trace class
    trace = OSITrace(args.data, args.type)

    if not args.output:
        path = pathlib.Path(args.data).with_suffix(".txth")
        args.output = str(path)

    with open(args.output, "wt") as f:
        for message in trace:
            f.write(str(message))

    trace.close()


if __name__ == "__main__":
    main()
