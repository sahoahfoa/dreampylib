#!/usr/bin/env python

# Very small example of the usage of DreamPyLib

import dreampylib

def main():

    # Dreamhost test API account:
    user = 'apitest@dreamhost.com'
    key  = '6SHU5P2HLDAYECUM'

    # Initialize the library and open a connection
    connection = dreampylib.DreampyLib(user,key)
       
    # If the connection is up, do some tests.
    if not connection.is_connected():
        print("Error connecting!")
        print(connection.status())
        return
        
    # For instance, list the available commands:
    print('Available commands:\n ')
    commands = connection.available_commands()
    command_names = [command[0] for command in commands]
    print('\n  '.join(command_names))
    
    print(connection.dreamhost_ps.list_ps())
    
    connection.dreamhost_ps.list_size_history(ps = 'ps7093')
    print(connection.result_list())
    
    # Let's also print(the keys so we know what we're looking at
    print(connection.result_keys())

if __name__ == '__main__':
    main()
