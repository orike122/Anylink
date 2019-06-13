# Anylink
Hello and welcome to Anylink, an app that lets you access your file anywhere, anytime.
## Getting started
Let's begin with the installation.
### prerequisites
- node.js
- python 3.7
- paramiko
You can install paramiko with:
```
py -3 -m pip install paramiko
```
### Installation
First we will download the zip file of the latest release under releases tab.
Extract the files into a folder and you should see something like that:
```
---assets
    |
    |---electron
    |---client.py
    |---main.py
---install.py
```
Then run install.py like this
```
py -3 install.py --path <PATH>
```
\<PATH> specifies the installation directory path, remeber this path we'll access this directory later.
<br \>
<br \>
The installation should take a few minutes. The installer will install deps run the configuration program for you.
### Configuring
After the program opens, you will need to open th login tab, and log in to your anylink account. If you have not created an account yet, 
go into https://anylinknow.tk and create one. 
<br \>
<br \>
Next, you should move into the next tab, an ssh public key should be there. Copy the full key, open [Anylink](https://anylinknow.tk), 
login, and under settings add the new public key.

### launching
Double click main.py in the installation directory(remember the path from earlier), and there you go. <br/> The PC client should appear in the main page of the site.
