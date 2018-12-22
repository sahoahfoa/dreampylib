#!/usr/bin/env python3
"""Simple example of the usage of DreamPyLib"""

import dreampylib


def main():
    """Example of the usage of DreamPyLib"""
    # DreamHost test API:
    key = '6SHU5P2HLDAYECUM'

    # Initialize the library and open a connection
    connection = dreampylib.DreampyLib(key)

    # If the connection is up, do some tests.
    if not connection.is_connected():
        print("Error connecting!")
        print(connection.status())
        return

    # For instance, list the available commands:
    print('Available commands:\n ')
    commands = connection.available_commands()
    command_names = [command['cmd'] for command in commands]
    print('\n'.join(command_names))

    success, _, body = connection.announcement_list.list_lists()
    if not success:
        raise Exception("Failed to list announcement lists.")
    print(body)

    for announcement_list in body:
        if int(announcement_list['num_subscribers']) < 200:
            connection.announcement_list.list_subscribers(
                listname=announcement_list['listname'],
                domain=announcement_list['domain'])

if __name__ == '__main__':
    main()
