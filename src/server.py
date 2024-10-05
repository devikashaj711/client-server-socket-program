"""
Server creates a socket for communicating with the client
Developed by 
Devika Shaj UMID: 2253223
Aysha Gulshan UMID: 14620948
"""
# Importing required  libraries
import socket
import json
import re

#Declaring the global variable
client_socket = None
command_words = []
record_exist = False
  
  
def main() :
    """Main function to initialise socket object and start listening  
    """
    # Define the server port
    SERVER_PORT = 2223

    #Defining global variable
    global client_socket
    
    try : 
        # Create a socket object and bind it to the server port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address

        server_socket.bind(('0.0.0.0', SERVER_PORT))
        server_socket.listen(5)  # Start listening for connections
        print(f"Server listening on port {SERVER_PORT}...")
        
    except socket.error as binding_error:
        print(f"Error in setting up socket: {binding_error}")
    
    try : 
        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            
            # Start a new thread to handle this client 
            res = handleClientServerConnection(client_socket)
            if res == "SHUTDOWN":
                break
    except socket.error as accept_error:
            print(f"Error in accepting the socket: {accept_error}")


def handleClientServerConnection(client_socket):
    """Function to handle the client server connection  
    """
    while True:
        try:
            client_data = client_socket.recv(1024).decode().strip()
            if not client_data:
                break
            print(f"Received command: {client_data}")
            res = handle_command_operations(client_data, client_socket)
            if res == "SHUTDOWN":
                return "SHUTDOWN"           
        except socket.error as accept_error:
            print(f"Error in handling the connection: {accept_error}")
            break

    # Close client socket after handling
    client_socket.close()
      

def handle_command_operations(input_command, client_socket):
    """Defining a method to handle address book command operations
    """

    #Declaring command word globally
    global command_words  
    
    # spliting the input command to words to perform the actual operations
    command_words = input_command.split()
    command_length = len(command_words)
    single_command = command_words[0]

    #To read the records from the address book
    current_address_data = load_record_read(client_socket)
    record_length = len(current_address_data)
    
    # Calling respective functions for every defined commands 
    if single_command == "ADD" and command_length == 4:
        add_record(current_address_data,record_length) 
        
    elif single_command == "LIST" and command_length == 1:
        list_records(current_address_data,record_length)
        
    elif single_command == "DELETE" and command_length == 2:
        delete_records(current_address_data,record_length)
        
    elif single_command == "SHUTDOWN" and command_length == 1:
        shutdown_server()
        return "SHUTDOWN"
    
    elif single_command == "QUIT" and command_length == 1:
        quit_client()
    else:
        client_socket.send(b"300 invalid command")     
 
            
def load_record_write(current_data):
    """Function to write records into address book
    """
    try :
        with open('data.json', 'w') as file:
            json.dump(current_data, file)

    except FileNotFoundError:
        print(f"ERROR File not found")
                    
            
def load_record_read(client_socket):
    """Function to load address book in read mode
    """
    try :
        with open('data.json', 'r') as file:
            current_data = json.load(file)
            return current_data
        
    except FileNotFoundError:
        print(f"File not found")
        client_socket.send(b"ERROR File not found")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        client_socket.send(b"ERROR File corrupted")


def delete_records(current_address_data,address_record_length):
    """Function to delete record in the address book
    """
    try:
        if address_record_length > 0 :
            delete_id = command_words[1]
            record_removed = []
            record_exist = False
            for delete_record in current_address_data:
                if delete_record['id'] == delete_id:
                    record_exist = True
                    record_removed =  delete_record
                    break            
                                        
            if record_exist == True :
                current_address_data.remove(record_removed)
                load_record_write(current_address_data)
                client_socket.send(b"200 OK")
            else :
                client_socket.send(b"No such record exists")  
        else:
            client_socket.send(b"Address book is empty, deletion not possible")

    except socket.error:
        print(f"ERROR Unable to delete")  


def list_records(current_address_data,address_record_length):
    """ Function to list record in the address book
    """
    try: 
        if address_record_length > 0 :
            response = "200 OK\nThe list of records in the book:\n"
            for record in current_address_data:
                response += f"{record['id']}\t {record['first name']} {record['last_name']}\t {record['phone_number']}\n"
            client_socket.send(response.encode() )
        else:
            client_socket.send(b"Address book is empty")

    except socket.error:
        print(f"ERROR Unable to list")  
            

def add_record(current_address_data,address_record_length):
    """Function to add record in the address book
    """
    try:
        if address_record_length < 20:
            if current_address_data and address_record_length != 0 :
                last_record = current_address_data[-1]
                last_record_id = int(last_record['id'])
                id =  last_record_id + 1 
            else:
                current_address_data = []    
                id = 1001  

            if command_words[1].isalpha() and command_words[2].isalpha() and re.fullmatch(r'^\d+(-\d+)*$', command_words[3]) :
                if len(command_words[1])<= 8 and len(command_words[2])<=8 and len(command_words[3]) == 12: 
                    data_block = {
                        "id": str(id),
                        "first name": command_words[1],
                        "last_name": command_words[2],
                        "phone_number": command_words[3]
                    }    
                    current_address_data.append(data_block)
                    load_record_write(current_address_data)
                    client_socket.send(f"200 OK \nThe new record Id is {id}".encode())
                else:
                    client_socket.send(b"Unable to add, invalid data")
            else:
                client_socket.send(b"Unable to add, invalid data")
        else:
            client_socket.send(b"The Address book is full with 20 records, so unable to add record")

    except socket.error:
        print(f"ERROR Unable to add") 


def shutdown_server(): 
    """Function to shutdown the server
    """
    try:  
        client_socket.send(b"200 OK")
        client_socket.close()  

    except socket.error as socket_error:
        print(f"ERROR Unable to shutdown") 


def quit_client(): 
    """Function to quit the client
    """
    try:
        client_socket.send(b"200 OK")   

    except socket.error as socket_error:
        print(f"Unable to quit: {socket_error}")


# Starting of the program
if __name__ == "__main__":
    client_handler = main()