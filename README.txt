                                            README for Server-Client Program
Project Overview
----------------

This program implements a simple server-client architecture, supporting five commands: ADD, DELETE, LIST, QUIT, and SHUTDOWN. 
The server listens for incoming connections, handles commands from clients, and processes them accordingly. 
The client connects to the server and sends commands as per user input. 
Both client and server handle errors and ensure proper termination of connections.


Technologies Used
-----------------

Language: Python 3
Networking: Socket programming (TCP)
Data Storage: JSON file for storing address book records


Commands Implemented
--------------------

ADD <item>: Adds a record in the address book.
DELETE <item>: Deletes a specified record from the address book.
LIST: Lists all records stored in the address book.
SHUTDOWN: Shuts down the server after closing all open connections and files.
QUIT: Closes the connection for the client, but keeps the server running.


Error Handling
--------------

The server handles invalid or malformed commands without crashing.
If an invalid command is sent, the server responds with an error message "300 Invalid command", and the connection remains active.
If the server encounters an error during operation, it logs the error and continues to run, unless a critical error occurs that requires a shutdown.
Clients that disconnect unexpectedly will not crash the server, which will continue to allow new clients to connect.


Running the Program

Prerequisites
-------------

Make sure you have the following before running the application:

1. Python installed on your system.
2. Both the client and server Python files (`client.py` and `server.py`).
3. A JSON file `data.json` created in the same directory where the server is running.
4. Ensure both the client and server can communicate on the same network.

Compilation and Execution
-------------------------

This project does not require compilation, but it needs to be executed in a Python environment.

Running the Server

To run the server, navigate to the directory containing the server script and run:
python3 server.py
You will see the below text in the terminal
Server listening on port <port number>...
The server will start and wait for clients to connect.


Running the Client

To run the client, navigate to the directory containing the client script and run:
python3 client.py <IP address>
You will see the below text in the terminal
Connected to <IP address> on port <port number>
C:
You will see the below text in the Server terminal
Accepted connection from ('127.0.0.1', 64597)


To implement ADD command

In the Client terminal, enter the below text
C: ADD <first-name> <last-name> <phone-number>
Once the record is added, the server will send the below message
S: 200 OK
The new record Id is <id>
If the command is not in the specified formatt, server will take it as a invalid command
Max of only 20 records can be added. If you try to add more than 20, it will show "The Address book is full with 20 records, so unable to add record" message 


To implement LIST command

In the Client terminal, enter the below text
C: LIST
Once the command is received by the server, it will send the list to the client as below
S 200 OK
The list of records in the book is:
<id> <first-name> <last-name> <phone-number>
If the command is not in the specified format, server will take it as a invalid command


To implement DELETE command

In the Client terminal, enter the below text
C: DELETE <id>
Once the command is received by the server, it will delete the record based on the id sent by the client as below
S 200 OK
If the command is not in the specified format, server will take it as a invalid command
If you try to delete a record that does not exists, it will show "No such record exist" message
If you try to delete a record from an empty address book, it will show "Address book is empty, deleteion not possible" message


To implement SHUTDOWN command

In the Client terminal, enter the below text
C: SHUTDOWN
Once the command is received by the server, it will terminate both the server and client
S 200 OK


To implement QUIT command

In the Client terminal, enter the below text
C: QUIT
Once the command is received by the server, it will terminate client
S 200 OK


Output
------

Output for Add
--------------
C: ADD DEVIKA SHAJ 456-345-3456
S 200 OK
The new record Id is 1001

C: ADD AYSHA GULSHAN 786-675-5678
S 200 OK
The new record Id is 1002

Output for List
---------------
C: LIST
S 200 OK
The list of records in the book is:
1001     DEVIKA SHAJ     456-345-3456
1002     AYSHA GULSHAN   786-675-5678
1003     AYZIN RAMZI     897-678-5433


Output for Delete
-----------------
C: DELETE 1003
S 200 OK


Output for Shutdown 
-------------------
C: SHUTDOWN
S 200 OK


Output for Quit 
-------------------
C: QUIT
S 200 OK


Output for Invalid command
--------------------------
C: DELETE
S 300 invalid command


