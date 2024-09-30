import socket
import sys
import json

# Define the server port
SERVER_PORT = 2223

# Check the number of command line arguments
if len(sys.argv) < 2:
    print("Usage: client <Server IP Address>")
    sys.exit(1)

server_ip = sys.argv[1]

# Initialize the client socket, input/output streams
try:
    # Try to open a socket to the server
    client_socket = socket.create_connection((server_ip, SERVER_PORT))
    print(f"Connected to {server_ip} on port {SERVER_PORT}")

    # Use the socket's file interface to read and write
    client_input = client_socket.makefile('r')
    client_output = client_socket.makefile('w')

    # Get input from the user through the terminal (stdin)
    std_input = sys.stdin

    # Communicate with the server by sending user input and receiving server response
    while True:
        user_input = input("Enter message: ")
        
        if not user_input:
            break  # Exit if input is empty

        client_output.write(user_input + '\n')
        client_output.flush()

        # Read server's response and print it
        server_input = client_input.readline()
        if not server_input:
            break  # Exit if no response from server
        
        # check command and command format
        input_command = server_input.strip()
        command_words = input_command.split()
        command_length = len(command_words)
        command = command_words[0]
        
        # switch function for address book operations
        def command_operations(command):
            if(command == "QUIT" and command_length == 1) :
                quit_client()
        
        # function to quit the client
        def quit_client(): 
            exit()
        
        # function call to do address command operations   
        command_operations(command)    
        
    # Close input/output streams and socket
    client_input.close()
    client_output.close()
    client_socket.close()

except socket.gaierror:
    print(f"Could not resolve the host: {server_ip}")
except ConnectionError:
    print(f"Could not connect to the server at {server_ip}")
except Exception as e:
    print(f"Error: {e}")
