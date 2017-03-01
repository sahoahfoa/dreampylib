#!/usr/bin/env python

# Very small example of the usage of DreamPyLib

import dreampylib

def main():

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
    command_names = [command[0] for command in commands]
    print('\n'.join(command_names))

    success, msg, body = connection.announcement_list.list_lists()
    if not success:
        raise Exception("Failed to list announcement lists.")
    print(body)

    for announcement_list in body:
        if int(announcement_list['num_subscribers']) < 200:
            connection.announcement_list.list_subscribers(listname=announcement_list['listname'], domain=announcement_list['domain'])
            print(connection.result_list())
    
            # Let's also print(the keys so we know what we're looking at
            print(connection.result_keys())

if __name__ == '__main__':
    main()
