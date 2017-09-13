import argparse
import locale
import sys

from . import translator


def print_results(result, extra_data, verbose=False):
    if verbose:
        print("Translated from {} to {}".format(extra_data["source"], extra_data["target"]))
    print(result)


def main():
    parser = argparse.ArgumentParser(description="Translate text to other languages using deepl.com")
    parser.add_argument("-s", "--source", help="Source language", metavar="lang")
    parser.add_argument("-t", "--target", help="Target language", metavar="lang")
    parser.add_argument("-v", "--verbose", help="Print additional information", action="store_true")
    parser.add_argument("text", nargs='*')

    args = parser.parse_args()

    locale_ = locale.getdefaultlocale()
    preferred_langs = [locale_[0].split("_")[0].upper()]

    if not args.source is None:
        source = args.source.upper()
    else:
        source = 'auto'
    if not args.target is None:
        target = args.target.upper()
    else:
        target = None

    if len(args.text) == 0:
        if sys.stdin.isatty():
            print("Please input text to translate")
            while True:
                text = input("> ")
                result, extra_data = translator.translate(text, source, target, preferred_langs)
                print_results(result, extra_data, args.verbose)

                if extra_data["source"] not in preferred_langs:
                    preferred_langs.append(extra_data["source"])
                if extra_data["target"] not in preferred_langs:
                    preferred_langs.append(extra_data["target"])
        else:
            text = sys.stdin.read()
            result, extra_data = translator.translate(text, source, target, preferred_langs)
            print_results(result, extra_data, args.verbose)

    else:
        text = " ".join(args.text)
        result, extra_data = translator.translate(text, source, target, preferred_langs)
        print_results(result, extra_data, args.verbose)


if __name__ == "__main__":
    main()