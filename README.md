sshpass
=======

If you need to login to a server that, for whatever reason, has public key auth disabled, you can use this script
to automate login via username nad password.

Your password will be stored in the appropriate keyring backend. (e.g. Keychain on Mac OS X)

Requires:

* Python
* pip (or easy_install)

pip install pexpect
pip install keyring


