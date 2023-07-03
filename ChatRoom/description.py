import sys, time

project_description = '''
 *********************************************************************

 Welcome to the client-server tcp chat room...
 
 ###################################
 
 Author     :    Sarthak Singh
 Version    :    1.0.1
 Language   :    Python
 Program    :    TCP Chat Room
 Year       :    2022
 Modules    :    customtkitner, threading, tkinter, os, time, PIL, socket, random

 ####################################

 *************************************************
'''
steps = '''
 Steps to run the server and client...
 
 1. Run the server file.
 2. Run the client file.
 3. Then again open another instance of client file...
 4. Enter your user name, password
 5. Choose your avator and then click next
 
 And type your message and press enter to send...
 '''

notes = '''
 Note : - (.py for the programmers and .exe for the common users...)
 Please do not run the (.py) file if you don't have Python installed in your computer...
'''

for letter in project_description:
    time.sleep(0.05)
    sys.stdout.write(letter)
    sys.stdout.flush()

for step in steps:
    time.sleep(0.06)
    sys.stdout.write(step)
    sys.stdout.flush()

for note in notes:
    time.sleep(0.05)
    sys.stdout.write(note)
    sys.stdout.flush()

input("\n\nPress any key to exit.............\n\n")