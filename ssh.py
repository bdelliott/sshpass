#!/usr/bin/env python

''' Automate SSH logins when you're force to authenticate with a password. '''
import getpass
import optparse
import os
import sys

import keyring
import pexpect

def getpassword(service, username):
    ''' Get password from keychain '''
    
    password = keyring.get_password(service, username)

    while not password:
        # ask and save a password.
        password = getpass.getpass("password: ")
        if not password:
            print "Please enter a password"

    return password

def setpassword(service, username, password):
    ''' Save password in keychain '''

    if not keyring.get_password(service, username):
        print "Successful login - saving password for user %s under keychain service '%s'" % (username, keychainservice)
        keyring.set_password(keychainservice, username, password)

    
def ssh(username, host, keychainservice="ssh_py_default", port=22):
    ''' Automate sending password when the server has public key auth disabled '''

    password = getpassword(keychainservice, username)

    print "Connecting to %s@%s" % (username, host)

    cmd = "/usr/bin/ssh -p%d %s@%s" % (port, username, host)
    child = pexpect.spawn(cmd)

    # handle the host acceptance and password crap.
    i = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'assword:'])
    if i == 0:
        # accept the host
        print "New server, accept the host..."
        child.sendline('yes')
        child.expect('assword:')

    print "Sending password"
    child.sendline(password)

    # assume we see a shell prompt ending in $ to denote successful login:
    print "Waiting for $ shell prompt terminator to confirm login..."
    if child.expect(r'\$') == 0:
        setpassword(keychainservice, username, password)

    # give control to the human.
    child.sendline()
    child.interact()

if __name__=='__main__':
    parser = optparse.OptionParser(usage="ssh.py [options] <username@>host")

    parser.add_option("-k", "--keychainservice", dest="keychainservice", help="Keychain service name to store password under", 
                     default="ssh_py_default")
    parser.add_option("-p", "--port", dest="port", help="SSH port", default=22)

    (opts, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_usage()
        sys.exit(1)

    host_str = args[0]
    if host_str.find("@") != -1:
        (username, host) = host_str.split("@")
    else:
        username = os.getlogin() # default to username on the current host.
        host = host_str

    ssh(username, host, port=int(opts.port), keychainservice=opts.keychainservice)



