#!/bin/bash

# Prompt the user to enter a command
echo "curl -k -d 'username=root@pam' --data-urlencode 'password=cyb3rbully' https://192.168.1.107:8006/api2/json/access/ticket"
read user_command

# Execute the command and append the output to output.txt
$user_command >> output.txt 2>&1

# Notify the user that the output has been saved
echo "The output has been appended to output.txt"f