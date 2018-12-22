#!/usr/bin/env python3
"""
Execute a DreamHost API command
"""
import sys
import argparse
import logging
import pprint
import json
import dreampylib

LOGGER = logging.getLogger("dh_run")
PP = pprint.PrettyPrinter(indent=4)


# https://stackoverflow.com/a/40389411
def printTable(myDict, col_list=None):
    """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
    If column names (col_list) aren't specified, they will show in random order.
    Author: Thierry Husson - Use it as you want but don't blame me.
    """
    if not isinstance(myDict, list) and not isinstance(myDict[0], dict):
        PP.pprint(myDict)
        return
    if not col_list:
        col_list = sorted(list(myDict[0].keys() if myDict else []))
    myList = [col_list]  # 1st row = header
    for item in myDict:
        myList.append([str(item[col] or "") for col in col_list])
    colSize = [max(map(len, col)) for col in zip(*myList)]
    formatStr = " | ".join(["{{:<{}}}".format(i) for i in colSize])
    myList.insert(1, ["-" * i for i in colSize])  # Seperating line
    for item in myList:
        print(formatStr.format(*item))


def main():
    """
    Execute a DreamHost API command
    """
    logging.basicConfig()

    parser = argparse.ArgumentParser(
        description="Execute a DreamHost API command",
        epilog="If your API command requires arguments add them after the command "
               "like so: --param value. Ex. dh_run apikeygoeshere dns.add_record "
               "--record test.example.com --value \"Don't PANIC\" --type TXT"
    )
    parser.add_argument("apikey", help="Dreamhost API key")
    parser.add_argument("cmd", help="Dreamhost API command")
    parser.add_argument("--json", action="store_true", help="Output json instead of table")
    parser.add_argument("--verbose", "-v", action="store_true", help="Make logging more verbose")

    args, unknown = parser.parse_known_args()

    for arg in unknown:
        if arg.startswith(("-", "--")):
            parser.add_argument(arg)

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    apikey = args.apikey
    cmd_name = args.cmd
    cmd_values = vars(args)
    output_json = args.json
    del cmd_values["apikey"]
    del cmd_values["cmd"]
    del cmd_values["json"]

    col_list = cmd_values.pop("collist", None)
    if col_list:
        col_list = [ele.strip() for ele in col_list.split(',')]

    connection = dreampylib.DreampyLib(apikey)

    if not connection.is_connected():
        LOGGER.info("Unable to connect")
        sys.exit(1)

    command = getattr(connection, cmd_name)

    success, msg, body = command(**cmd_values)
    if success:
        LOGGER.info("%s - %s" % (cmd_name, msg))
    else:
        LOGGER.info("%s" % (msg))
        sys.exit(1)

    if output_json:
        print(json.dumps(body, indent=4, sort_keys=True))
    else:
        printTable(body, col_list)


if __name__ == "__main__":
    main()
