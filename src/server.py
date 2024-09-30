import socket
import json

# Define the server port
SERVER_PORT = 2223

# Create a socket object and bind it to the server port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address

server_socket.bind(('0.0.0.0', SERVER_PORT))
server_socket.listen(5)  # Start listening for connections

print(f"Server listening on port {SERVER_PORT}...")

while True:
    try:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Open input and output streams
        client_input = client_socket.makefile('r')
        client_output = client_socket.makefile('w')

        # As long as we receive data, echo that data back to the client
        while True:
            input_command_line = client_input.readline()
            if not input_command_line:
                break  # Exit the loop if no data is received

            print(f"New Record Received: {input_command_line}")

            #TODO
            # check command and command format
            input_command = input_command_line.strip()
            command_words = input_command.split()
            command_length = len(command_words)
            command = command_words[0]
            print("command:", command, command_length)

            #variable denote the record exist in addressbook or not
            record_exist = False

            # function to add record in the address book
            def add_record():
                current_address_data = load_record_read()
                address_record_length = len(current_address_data)
                if address_record_length  < 20:
                    print("The length less than ",len(current_address_data))
                    try: 
                        if current_address_data :
                            last_record = current_address_data[-1]
                            last_record_id = int(last_record['id'])
                            id =  last_record_id + 1
                            print("inside with ",last_record_id) 
                         
                    except :  
                        current_address_data = [] 
                        id = 1001
                        print("inside except ",id) 
                    
                    data_block = {
                        "id": str(id),
                        "first name": command_words[1],
                        "last_name": command_words[2],
                        "phone_number": command_words[3]
                    }
                    current_address_data.append(data_block)
                    print("200 OK")
                    print("the new record Id is",id)
                    print()
                    load_record_write(current_address_data)
                else:
                    print("The address book already contains 20 records")

            # function to list record in the address book
            def list_records():
                current_address_data = load_record_read()
                print("200 OK")
                print("The list of records in the book:")
                for record in current_address_data:
                    print(f" {record['id']}   {record['first name']} {record['last_name']}   {record['phone_number']}")
            
            # function to delete record in the address book
            def delete_records():
                current_address_data = load_record_read()
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
                    print("200 OK")
                    print("the deleted record is", delete_id)
                else :
                    print("no such record exist ")  

            # function to shutdown the server
            def shutdown_server():   
                print("200 OK")
                client_output.flush()
                server_socket.close()
                exit(0)

            # function to quit the client
            def quit_client(): 
                print("200 OK")
            
            
            # function to load address book in write mode
            def load_record_write(current_data):
                print("load_record_write ")

                with open('data.json', 'w') as file:
                    json.dump(current_data, file)
            
            
            # function to load address book in read mode
            def load_record_read():
                 print("load_record_read ")
                 with open('data.json', 'r') as file:
                    current_data = json.load(file)
                    return current_data
            

            
            # switch function for address book operations
            def command_operations(command):
                if command == "ADD" and command_length == 4:
                    add_record() 
                elif command == "LIST" and command_length == 1:
                    list_records()
                elif command == "DELETE" and command_length == 2:
                    delete_records()
                elif command == "SHUTDOWN" and command_length == 1:
                    shutdown_server()
                elif command == "QUIT" and command_length == 1:
                    quit_client()
                else:
                    print("300 invalid command")
            
            # function call to do address command operations   
            command_operations(command)    
                          
           

            client_text = input_command_line.strip()
            client_output.write(input_command_line)
            client_output.flush()

        # Close the input, output streams and socket
        client_input.close()
        client_output.close()
        client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
