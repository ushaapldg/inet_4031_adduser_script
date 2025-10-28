#!/usr/bin/python3

# INET4031
# Usha Paladugu
# 10/17/2025
# 10/28/2025

import os    #Allows the python code to access and run the OS(Linux in this case)
import re    #Used for expression matching to filter out comments in the code
import sys   #Used to read input from the standard input

def main():
    for line in sys.stdin:

        #Skip lines starting with '#' (aka skips reading in comments)
        match = re.match("^#", line)

        print("The contents of the match variable were: ", match)

        #This splits the input line into fields using ':' so we can extract individual pieces of user data
        fields = line.strip().split(':')

        print("The length of fields was: ", len(fields))

        #This IF statement skips lines that are either comments or don't have exactly 5 fields
        #It relies on the previous two steps: checking for comment lines and splitting the line into fields
        #If the IF statement evaluates to true, the line is ignored and the loop continues to the next line
        if match or len(fields) != 5:
            continue

        #These lines get the username and password, and format the GECOS field as "First Last,,,"
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        #This splits the fifth field into a list of groups the user should be added to
        groups = fields[4].split(',')

        #This prints a message to indicate that a new user account is being created
        print("==> Creating account for %s..." % (username))

        #This builds the command to create the user with the specified GECOS info and no initial password
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)

        #Uncomment this code first time it is being run
        print(cmd)
        os.system(cmd)

        #This prints a message to indicate that the password is being set for the user
        print("==> Setting the password for %s..." % (username))

        #This builds the command to set the user's password using echo piped into passwd
        cmd = "/bin/echo -ne '%s\n%s\n' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)

        #Uncomment this code first time it is being run
        print(cmd)
        os.system(cmd)

        for group in groups:
            #This checks if the group is not a placeholder ('-') and assigns the user to that group
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()

