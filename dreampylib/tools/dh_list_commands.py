#!/usr/bin/env python3
"""List command available with provided API key"""

import argparse
import dreampylib


def main():
    """List command available with provided API key"""
    parser = argparse.ArgumentParser()
    parser.add_argument('apikey', help='Your dreamhost API key')
    args = parser.parse_args()

    connection = dreampylib.DreampyLib(args.apikey)
    if not connection.is_connected():
        raise Exception("Unable to connect")

    print(", ".join(dir(connection)))

if __name__ == '__main__':
    main()
