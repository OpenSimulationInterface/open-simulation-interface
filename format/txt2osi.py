'''
This program converts txt trace files separated with $$__$$ to OSI trace files which are defined by the length of each OSI message. 

Example usage:
    python3 txt2osi.py -d trace.txt
    python3 txt2osi.py -d trace.txt -o myfile
    python3 txt2osi.py -d trace.txt -o myfile -c
    python3 txt2osi.py -d trace.txt.lzma -c
    python3 txt2osi.py -d trace.txt.lzma
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
                        description='Convert txt trace file to osi trace files.',
                        prog='txt2osi converter')
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
                        default='converted.osi',
                        type=str,
                        required=False)
    parser.add_argument('--compress', '-c',
                        help='Compress the output to a lzma file.',
                        default=False,
                        required=False,
                        action="store_true")

    return parser.parse_args()

def main():
    # Handling of command line arguments
    args = command_line_arguments()

    # Initialize the OSI trace class
    trace = OSITrace()
    trace.from_file(path=args.data, type_name=args.type, format_type='separated')
    sv = trace.get_messages() # Create an iterator for messages

    args.output = args.output.split('.', 1)[0] + '.osi'

    if args.output == 'converted.osi':
        args.output = args.data.split('.', 1)[0] + '.osi'

    if args.compress:
        f = lzma.open(args.output + '.lzma', "ab")
    else:
        f = open(args.output, "ab")
    
    for message in sv:
        byte_buffer = message.SerializeToString()
        f.write(struct.pack("<L", len(byte_buffer)) + byte_buffer) 
    
    f.close()
 
if __name__ == "__main__":
    main()