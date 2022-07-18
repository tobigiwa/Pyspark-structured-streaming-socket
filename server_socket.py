import socket
import time

host = socket.gethostbyname(socket.gethostname())
port = 5011
flag = True

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket_obj:
        server_socket_obj.bind((host, port))
        server_socket_obj.listen(5)
        print('Open to received connection...\n')
        conn_obj, addr = server_socket_obj.accept()  # we did'nt add this in the `whille loop` as mostly seen since we are expecting just one connection
        print(F'Got connection from {addr}.\n')

        while flag:
            with conn_obj:
                with open('files/text_file.txt', 'r') as file_handler:
                    for lines in file_handler:
                        conn_obj.send(bytes(f'{lines}', 'utf-8'))
                        time.sleep(3)
                    else:
                        print('End of file(EOF) reached.\n')
                        flag = False # we we got here our text file is already exhausted

        server_socket_obj.shutdown(socket.SHUT_RDWR)
        # our context manager would manage the `server_socket_obj.close()`

except socket.error as err:
    print('\n\nSocket error: \n', err)

else:
    print('All went good...\n')

finally:
    print('Server connection successfully shutdown.')