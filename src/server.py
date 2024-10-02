import socket
import json
import threading
import sys
import os

client_socket = None
command_words = []
record_exist = False
      
def main() :
    # Define the server port
    SERVER_PORT = 2223
    global client_socket
    global server_socket
    # Create a socket object and bind it to the server port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address

    server_socket.bind(('0.0.0.0', SERVER_PORT))
    server_socket.listen(5)  # Start listening for connections

    print(f"Server listening on port {SERVER_PORT}...")
    
    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        
        # Start a new thread to handle this client
        res = handleClientServerConnection(client_socket)
        if res == "SHUTDOWN":
            break


def handleClientServerConnection(client_socket):
    while True:
        try:
            client_data = client_socket.recv(1024).decode().strip()
            if not client_data:
                break
            print(f"Received command: {client_data}")
            res = handle_command_operations(client_data, client_socket)
            if res == "SHUTDOWN":
                return "SHUTDOWN"                
        except:
            break
    # Close client socket after handling
    client_socket.close()
      

def handle_command_operations(input_command, client_socket):
    global command_words
    command_words = input_command.split()
    command_length = len(command_words)
    single_command = command_words[0]
    if single_command == "ADD" and command_length == 4:
        add_record() 
    elif single_command == "LIST" and command_length == 1:
        list_records()
    elif single_command == "DELETE" and command_length == 2:
        delete_records()
    elif single_command == "SHUTDOWN" and command_length == 1:
        shutdown_server()
        return "SHUTDOWN"
    elif single_command == "QUIT" and command_length == 1:
        quit_client()
    else:
        client_socket.send(b"300 invalid command")     
 
            
# function to load address book in write mode
def load_record_write(current_data):
    with open('data.json', 'w') as file:
        json.dump(current_data, file)
            
            
# function to load address book in read mode
def load_record_read():
    with open('data.json', 'r') as file:
        current_data = json.load(file)
        return current_data   
    
# function to delete record in the address book
def delete_records():
    current_address_data = load_record_read()
    delete_address_length = len(current_address_data)
    if delete_address_length > 0 :
        print("delete_address_length greator than zero")
        delete_id = command_words[1]
        record_exist = False
        for delete_record in current_address_data:
            if delete_record['id'] == delete_id:
                record_removed = []
                record_exist = True
                record_removed =  delete_record
                break            
                                    
        if record_exist == True :
            current_address_data.remove(record_removed)
            load_record_write(current_address_data)
            client_socket.send(b"200 OK")
            print("the deleted record is", delete_id)
        else :
            client_socket.send(b"No such record exist")  
    else:
        client_socket.send(b"Address book is empty")
        
# function to list record in the address book
def list_records():
    current_address_data = load_record_read()
    delete_address_length = len(current_address_data)
    
    if delete_address_length > 0 :
        response = "200 OK\nThe list of records in the book is:\n"
        for record in current_address_data:
            response += f"{record['id']} {record['first name']} {record['last_name']} {record['phone_number']}\n"
        client_socket.send(response.encode() )
    else:
        client_socket.send(b"Address book is empty")
            
# function to add record in the address book
def add_record():
    current_address_data = load_record_read()
    address_record_length = len(current_address_data)
    if address_record_length  < 20:
        if current_address_data and address_record_length != 0 :
            last_record = current_address_data[-1]
            last_record_id = int(last_record['id'])
            id =  last_record_id + 1 
        else:
            current_address_data = []    
            id = 1001  

        data_block = {
            "id": str(id),
            "first name": command_words[1],
            "last_name": command_words[2],
            "phone_number": command_words[3]
        }    
        current_address_data.append(data_block)
        load_record_write(current_address_data)
        client_socket.send(f"200 OK \n The new record Id is {id}".encode())
    else:
        client_socket.send(b"The Address book is full with 20 records")

# function to shutdown the server
def shutdown_server():   
    client_socket.send(b"200 OK")
    client_socket.close()   

# function to quit the client
def quit_client(): 
    client_socket.send(b"200 OK")   
    client_socket.close()            
                         

if __name__ == "__main__":
    client_handler = main()