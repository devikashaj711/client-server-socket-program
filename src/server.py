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
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Open input and output streams
    client_input = client_socket.makefile('r')
    client_output = client_socket.makefile('w')

    # As long as we receive data, echo that data back to the client
    while True:
        line = client_input.readline()
        if not line:
            break  # Exit the loop if no data is received

        print(f"Received: {line}")

        #TODO
        # check command
        text = line.strip()
        command = text.split()[0]
        # print("command:", command)

        if command == "ADD" :

            
            try:
                    with open("data.json", "r") as file:
                        current_data = json.load(file)
                        id =  1001 + len(current_data)
            except:
                    current_data = [] 
                    id = 1001
                    print("new file")
                    print(current_data)
            
            data_block = {
                    "id": str(id),
                    "first name": text.split()[1],
                    "last_name": text.split()[2],
                    "phone_number": text.split()[3]
            }                
            current_data.append(data_block)
            with open('data.json', 'w') as file:
                    json.dump(current_data, file)

            print("200 OK")
            print("The new Record ID is", id)
            try:
                with open("data.json", "r") as file:
                    current_data = json.load(file)
                    
            except:
                current_data = [] 
                print("new file")
         

        
        if command == "LIST" :
            with open("data.json", "r") as file:
                current_data = json.load(file)

            for item in current_data:
                # print(item)
            

                print(item["id"], "\t", item["first name"], "", item["last_name"], "\t", item["phone_number"])



        if command == "DELETE" :
            with open("data.json", "r") as file:
                current_data = json.load(file)

            new_data = []
            id = text.split()[1]
            for item in current_data:
                print(item)
                if id == item["id"]:
                     
                     continue
                new_data.append(item) 
                # print(item["id"], "\t", item["first name"], "", item["last_name"], "\t", item["phone_number"])
                print("200 OK")

            with open('data.json', 'w') as file:
                json.dump(new_data, file) 
                    
                  
        if command == "SHUTDOWN" :
            print("200 OK")
            client_output.write(line)
            client_output.flush()
            client_input.close()
            client_output.close()
            client_socket.close()
            break

        if command == "QUIT" :
             print("200 OK")
       

        client_output.write(line)
        client_output.flush()
        

    # Close the input, output streams and socket

    client_input.close()
    client_output.close()
    client_socket.close()
    

