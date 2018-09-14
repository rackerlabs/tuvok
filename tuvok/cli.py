from tuvok import __version__
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v',
                        action='version',
                        version='version %s' % __version__)
    parser.add_argument('--hi', '-w', dest='hi',
                        help='Hi Everybody!!!',
                        required=False)

    args = parser.parse_args()

    if args.hi:
        print("Hi Everybody!!!")
        print("Hi {}!!!".format(args.hi))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
