import sys
import locale
import argparse

import translator


def print_results(result, verbose=False):
    if verbose:
        print("Translated from {} to {}".format(result["source"], result["target"]))
    print(result["translation"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text to other languages using deepl.com")
    parser.add_argument("-s", "--source", help="Source language", metavar="lang")
    parser.add_argument("-t", "--target", help="Target language", metavar="lang")
    parser.add_argument("-v", "--verbose", help="Print additional information", action="store_true")
    parser.add_argument("text", nargs='*')

    args = parser.parse_args()

    locale_ = locale.getdefaultlocale()
    default_lang = locale_[0].split("_")[0].upper()

    if len(args.text) == 0:
        if sys.stdin.isatty():
            print("Please input text to translate")
            while True:
                text = input("> ")
                result = translator.translate(text, args.source, args.target, args.verbose)
                print_results(result, args.verbose)
        else:
            text = sys.stdin.read()
            result = translator.translate(text, args.source, args.target, args.verbose)
            print_results(result, args.verbose)

    else:
        text = " ".join(args.text)
        result = translator.translate(text, args.source, args.target, args.verbose)
        print_results(result, args.verbose)