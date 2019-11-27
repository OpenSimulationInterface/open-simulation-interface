'''
This program converts serialized txt/osi trace files into a human readable txth file. 

Example usage:
    python3 osi2read.py -d trace.osi -o myreadableosifile
    python3 osi2read.py -d trace.txt -f separated -o myreadableosifile
'''

from OSITrace import OSITrace
import struct
import lzma
import argparse
import os

def command_line_arguments():
    """ Define and handle command line interface """

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser(
                        description='Convert a serialized osi/txt trace file to a readable txth output.',
                        prog='osi2read converter')
    parser.add_argument('--data', '-d',
                        help='Path to the file with serialized data.',
                        type=str)
    parser.add_argument('--type', '-t',
                        help='Name of the type used to serialize data.',
                        choices=['SensorView', 'GroundTruth', 'SensorData'],
                        default='SensorView',
                        type=str,
                        required=False)
    parser.add_argument('--output', '-o',
                        help='Output name of the file.',
                        default='converted.txth',
                        type=str,
                        required=False)
    parser.add_argument('--format', '-f',
                        help='Set the format type of the trace.',
                        choices=['separated', None],
                        default=None,
                        type=str,
                        required=False)

    return parser.parse_args()

def main():
    # Handling of command line arguments
    args = command_line_arguments()

    # Initialize the OSI trace class
    trace = OSITrace()
    trace.from_file(path=args.data, type_name=args.type, format_type=args.format)

    args.output = args.output.split('.', 1)[0] + '.txth'

    if args.output == 'converted.txth':
        args.output = args.data.split('.', 1)[0] + '.txth'

    trace.make_readable(args.output)    
 
if __name__ == "__main__":
    main()