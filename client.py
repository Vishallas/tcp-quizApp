import socket

def decode(encoded_bytes):
    decoded_dict = {}
    index = 0

    # To encode the question
    # Extract the key length (4 bytes) and convert it to an integer
    key_length = int.from_bytes(encoded_bytes[index:index+4], byteorder='big')
    index += 4

    # Extract the key using the key_length
    key = encoded_bytes[index:index+key_length].decode('utf-8')
    index += key_length

    # Extract the value length (4 bytes) and convert it to an integer
    value_length = int.from_bytes(encoded_bytes[index:index+4], byteorder='big')
    index += 4

    # Extract the value using the value_length
    value = encoded_bytes[index:index+value_length].decode('utf-8')
    index += value_length

    decoded_dict[key] = value

    # to encode choices
    choices = []

    key_length = int.from_bytes(encoded_bytes[index:index+4], byteorder='big')
    index += 4

    # Extract the key using the key_length
    key = encoded_bytes[index:index+key_length].decode('utf-8')
    index += key_length

    while index < len(encoded_bytes):
        value_length = int.from_bytes(encoded_bytes[index:index+4], byteorder='big')
        index += 4

        # Extract the value using the value_length
        value = encoded_bytes[index:index+value_length].decode('utf-8')
        index += value_length
        choices.append(value)

    decoded_dict[key] = choices

    return decoded_dict

def pprint(question):
    print('\n1) %s\r' % question['question'])
    for i in range(4):
        print(f"[{i+1}] {question['choices'][i]}")

    choice = int(input('\nEnter the choice : ').strip())

    input('\nConfirm the Choice %d, press enter.' % choice)

    return choice

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1111
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))


while True:
    try:
        # name_prompt = client_socket.recv(1024).decode('utf-8')
        # print(name_prompt, end='')

       
        name = input('Enter the id. : ')
        client_socket.send(name.encode('utf-8'))
        
        print('Entering into the quiz....')
        NO_OF_QUES = int(client_socket.recv(1024).decode('utf-8'))

        for i in range(NO_OF_QUES):
            data = client_socket.recv(1024)
            if data != '':
                question = decode(data)
                choice = pprint(question)
                client_socket.send(str(choice).encode('utf-8'))

        client_socket.close()
        print("The test completed....")
        break
    except KeyboardInterrupt:
        print("Exited from test...")
        client_socket.close()
        break
    except Exception as e:
        print(e)
        client_socket.close()
        break
