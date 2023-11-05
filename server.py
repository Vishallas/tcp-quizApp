#!/usr/bin/env python

# modules
import socket
import threading
import random
import csv

def comput_bytes(data):
    data_bytes = data.encode('utf-8')
    bytes_length = len(data_bytes).to_bytes(4, byteorder='big')

    return data_bytes, bytes_length

def encode(data_dict):
    encoded_bytes = b""  # Initialize an empty byte string

    # value of question key
    value = data_dict[q_KEY]

    # converting question to bytes
    key_bytes, key_length_bytes = comput_bytes(q_KEY)
    value_bytes,value_length_bytes = comput_bytes(value)

    # Append the key length, key, value length, and value to the encoded bytes
    encoded_bytes += key_length_bytes + key_bytes + value_length_bytes + value_bytes

    # Converting to the choices to bytes
    bytes,length_bytes = comput_bytes(c_KEY)
    encoded_bytes += length_bytes + bytes

    # value of choice key
    value = data_dict[c_KEY]

    # converting the list of value to bytes
    for c in value:
        value_bytes, value_length_bytes = comput_bytes(c)
        encoded_bytes += value_length_bytes + value_bytes
    
    return encoded_bytes

def convertQtobQ(questions):
    bquestion = {}
    for i,j in questions.items():
        bquestion.setdefault(i,encode(j))
    return bquestion

def read_csv(file_name):
    with open('test_csv.csv') as f:
        k = csv.reader(f)
        q = {}
        next(k)
        for row in k:
            id = int(row[0])
            ques = row[1]
            chcs = row[2].split('*-/')
            q.setdefault(id,{})
            q[id].setdefault(q_KEY, ques)
            q[id].setdefault(c_KEY, chcs)
    return q

def handle_client(client_socket):
    
    try:
        client_id=client_socket.recv(1024).decode('utf-8')

        print(f'{client_id.upper()} connected')

        f = open(f'ans_dist/{client_id.upper()}.csv', 'w', newline="")
        k = csv.writer(f)
        k.writerow(['q_id', 'ans'])

        # Initialize the client with no of questions
        client_socket.send(str(NO_OF_QUES).encode('utf-8'))

        # sending questions
        for q_ID in random.sample(q_IDs,NO_OF_QUES):

            # Sending the question of particular question id
            client_socket.send(bquestion[q_ID])

            # receiving the choice sent by the client
            c = int(client_socket.recv(1024).decode('utf-8')) 

            print(f'the {client_id} give the choice {c} for question {q_ID}.')

            k.writerow([q_ID, c])

        print("%s completed." % client_id)
    except Exception as e:
        print(e)
        print("%s exits from test." % client_id)
    finally:
        client_socket.close()

# IP and port number
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1111

NO_OF_QUES = 5

q_KEY = 'question'
c_KEY = 'choices'

CLIENTS = ('21CS321', '21EE124','21EC231')

FILE_NAME = 'test_csv.csv'

questions = read_csv(FILE_NAME)

bquestion = convertQtobQ(questions)
q_IDs = list(questions.keys())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

while True:
    # print("Waiting for a client to connect...")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    
    # client_threads.append(client_thread)
    client_thread.start()
    