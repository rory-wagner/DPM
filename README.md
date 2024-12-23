# DPM (Deterministic Password Manager)

This is a web application (unhosted) that deterministically generates passwords for users.

Gone are the ways of storing passwords for hackers to attack! Instead, generate the passwords on the fly!

# Quick Start / How To Use:

Provide DPM with these fields:
```
Username: My name (e.g. Rory)
Master Password: The one password you need to remember (e.g. Password1234)
Domain: The website you are trying to log into (e.g. gmail.com)
Counter: The counter that you may tick up in case you need to reset a password (e.g. 4)
```
Once each of these fields are provided, you may select the following optional custom password settings that allow the generator to create the password with a guarantee that the password will follow those rules.
```
Length: The length of the resulting password (e.g. 12)
Symbols: A list of symbols to provide and at least 1 is guaranteed to appear (e.g. !@#$)
Uppercase: At least one uppercase letter will appear
Lowercase: At least one lowercase letter will appear
Numbers: At least one number will appear
```
Finally when you click either `Generate default password` (doesn't use Custom rules) or `Generate Custom` (does use Custom rules) a password like this should appear:

`@/=7YlE+1tE}@RjXOPPf`

## Local Setup BE:

The backend is run with Python3.x

It is suggested to use a venv and install all requirements in requirements.txt.

After activating venv and installing the requirements, run `python ./serverSide/server.py`
(Listens on port 8080)

## Local Setup FE:

The frontend was never intended to be big, so it is just an html page.

Simply navigate to the page in your browser.
