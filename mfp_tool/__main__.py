
import parser
import argparse
import os
import sys

import mfp_tool.stat as stat

if __name__ == "__main__":
    try:
        arg_parser = argparse.ArgumentParser(prog="MFP Prediction Tool")
        arg_parser.add_argument("--path", help="Directory path for memory failure logs.", required=True)
        arg_parser.add_argument("--output", help="File path for store MFP evaluation result.", required=False, default=None)
        arg_parser.add_argument("--cpu", help="Multi processing number for running", required=False, default=1, type=int, choices=range(1, 129))
        args = arg_parser.parse_args()
    except argparse.ArgumentError:
        sys.stderr.write("Argument parse failed\n")
        sys.exit(1)

    try:
        if not os.path.isdir(args.path):
            sys.stderr.write("error: path is not directory or not exists\n")
            sys.exit(1)
        
        if args.output is None:
            args.output = 1
        else:
            try:
                args.output = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            except:
                sys.stderr.write("error: output file is not available\n")
                sys.exit(1)

        if not args.path.endswith("/"):
            args.path += "/"
        stat.stat(args)
    except:
        sys.stderr.write("internal error happened\n")
        raise
    finally:
        if type(args.output) is int and args.output >= 3:
            os.close(args.output)
