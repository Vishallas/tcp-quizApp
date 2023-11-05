#!/usr/bin/env python

# modules
import socket
import threading
import random


def encode(data_dict):
    encoded_bytes = b""  # Initialize an empty byte string

    q_key = 'question'
    value = data_dict[q_key]
    # Encode the q_key and value as strings, separated by a delimiter (e.g., '|')
    key_bytes = q_key.encode('utf-8')
    value_bytes = str(value).encode('utf-8')

    # Calculate the length of key and value, and convert to 4-byte integers
    key_length = len(key_bytes)
    value_length = len(value_bytes)

    key_length_bytes = key_length.to_bytes(4, byteorder='big')
    value_length_bytes = value_length.to_bytes(4, byteorder='big')

    # Append the key length, key, value length, and value to the encoded bytes
    encoded_bytes += key_length_bytes + key_bytes + value_length_bytes + value_bytes

    c_key = 'choices'
   
    key_bytes = c_key.encode('utf-8')
    key_length = len(key_bytes)
    key_length_bytes = key_length.to_bytes(4, byteorder='big')
    encoded_bytes += key_length_bytes + key_bytes

    value = data_dict[c_key]
    for c in value:
        value_bytes = c.encode()
        value_length = len(value_bytes)
        value_length_bytes = value_length.to_bytes(4, byteorder='big')
        encoded_bytes += value_length_bytes + value_bytes
    
    return encoded_bytes

def convertQtobQ(questions):
    bquestion = {}
    for i,j in questions.items():
        bquestion.setdefault(i,encode(j))
    return bquestion

def handle_client(client_socket,client_addr):
    
    try:
        # Username and file creation)
        user_question="Enter your Name: "
        client_socket.send(user_question.encode())
        username = client_socket.recv(1024).decode()

        print(f'{username} connected')

        client_socket.send(str(NO_OF_QUES).encode())
        t_q_IDs = q_IDs.copy()
        random.shuffle(t_q_IDs)

        for q_ID in random.sample(t_q_IDs,NO_OF_QUES):
            # json_str = json.dumps(questions[q_ID])
            # bytes_representation = json_str.encode()

            client_socket.send(bquestion[q_ID])
            c = int(client_socket.recv(1024).decode())  
            print(f'the {client_addr} give the choice {c} for question {q_ID}.')
        print("%s completed." % username)
        client_socket.close()
    except:
        print("%s exits from test." % username)
        client_socket.close()

# IP and port number
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1111

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)


NO_OF_QUES = 5
questions = {
    1: {
        'question': 'How are you',
        'choices': ['fine', 'not bad', 'good', 'can\'t disclose']
    },
    2: {
        'question': 'What is your name',
        'choices': ['Alice', 'Bob', 'Charlie', 'David']
    },
    3: {
        'question': 'Where are you from',
        'choices': ['USA', 'Canada', 'UK', 'Australia']
    },
    4: {
        'question': 'Favorite color',
        'choices': ['Red', 'Blue', 'Green', 'Yellow']
    },
    5: {
        'question': 'What is your favorite food',
        'choices': ['Pizza', 'Burger', 'Sushi', 'Pasta']
    },
    6: {
        'question': 'How do you like to spend your weekends',
        'choices': ['Reading', 'Hiking', 'Netflix', 'Gaming']
    },
    7: {
        'question': 'Favorite animal',
        'choices': ['Dog', 'Cat', 'Dolphin', 'Elephant']
    },
    8: {
        'question': 'Favorite movie genre',
        'choices': ['Action', 'Comedy', 'Drama', 'Science Fiction']
    },
    9: {
        'question': 'What\'s your dream travel destination',
        'choices': ['Paris', 'Tokyo', 'Hawaii', 'New York']
    },
    10: {
        'question': 'What\'s your preferred way of transportation',
        'choices': ['Car', 'Bicycle', 'Public Transit', 'Walking']
    },
    # Add more questions here as needed
}


bquestion = convertQtobQ(questions)
q_IDs = list(questions.keys())

while True:
    # print("Waiting for a client to connect...")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address,))
    
    # client_threads.append(client_thread)
    client_thread.start()


    