import socket

# Define the server port
SERVER_PORT = 2223

# Create a socket object and bind it to the server port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            line = client_input.readline()
            if not line:
                break  # Exit the loop if no data is received

            print(f"Received: {line.strip()}")

            # ADD text
            text = line.strip()
            # print(text)
            # text_split = text.split()

            # # fine line count
            # # append to first word
            # with open("database.txt", "r") as file:
            #     line_count = 1001
            #     # Loop through each line in the file
            #     for line in file:
            #         line_count += 1
            # print(line_count)

            # text_combined = str(line_count) + " " + text_split[1] + " " + text_split[2] + " " + text_split[3]
            # print("text_combined")
            # print(text_combined)
            # with open("database.txt", "a") as file:
            #     # Write a line of text to the file
                # file.write("\n" + text_combined)


            client_output.write(line)
            client_output.flush()

        # Close the input, output streams and socket
        client_input.close()
        client_output.close()
        client_socket.close()

    except Exception as e:
        print(f"Error: {e}")
