import argparse
import sys
import io
from argparse import Namespace

ENCODING = "utf-8"

def count_stream(stream: io.TextIOWrapper) -> tuple:
    num_lines = num_words = num_chars = num_bytes = 0
    for line in stream: 
        num_lines += 1                      
        num_words += len(line.split())
        num_chars += len(line)
        num_bytes += len(line.encode(ENCODING))

    return num_lines, num_words, num_chars, num_bytes


def main(stream: io.TextIOWrapper, args: Namespace) -> None:

    lines, words, chars, bbytes = count_stream(stream)

    filename = args.path if args.path != "-" else ""

    # Default behaviour: no flags -> print lines, words, chars 
    if not (args.lines or args.words or args.chars or args.bytes):
        print(f"{lines} {words} {chars} {filename}".strip())
        return

    output = []
    if args.bytes:
        output.append(str(bbytes))
    if args.lines:
        output.append(str(lines))
    if args.words:
        output.append(str(words))
    if args.chars:
        output.append(str(chars))
    
    if filename:
        output.append(filename)
    
    print(" ".join(output))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="-", help="read input from file; if path is '-', read from stdin")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-l", "--lines", action="store_true", help="print the number of lines")
    parser.add_argument("-w", "--words", action="store_true", help="print the number of words")
    parser.add_argument("-m", "--chars", action="store_true", help="print the number of characters")
    args = parser.parse_args()
    if args.path == "-":
        stream = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", newline='')
        main(stream, args)
    else:
        try:
            with open(args.path, mode="r", encoding="utf-8", newline='') as stream:
                main(stream, args)
        except FileNotFoundError as fnf:
            print(fnf)
        except Exception as e:
            print(f"Error: {e}")
    