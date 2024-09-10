import socket
import threading

# 모든 클라이언트 연결을 추적하는 리스트
clients = []
client_names = {}

# 클라이언트 메시지를 모든 클라이언트에 브로드캐스트하는 함수
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:  # 보낸 사람에게는 다시 보내지 않음
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

# 클라이언트 연결을 처리하는 함수
def handle_client(client_socket):
    try:
        # 처음에 클라이언트로부터 이름을 수신
        client_socket.send("Enter your name: ".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8')
        client_names[client_socket] = name
        broadcast(f"{name} has joined the chat.".encode('utf-8'), client_socket)

        while True:
            # 클라이언트의 메시지를 수신
            message = client_socket.recv(1024)
            if message:
                broadcast(f"{name}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
            else:
                # 클라이언트가 연결을 끊었을 경우
                client_socket.close()
                clients.remove(client_socket)
                broadcast(f"{name} has left the chat.".encode('utf-8'))
                break
    except:
        # 예외 발생 시 연결 종료
        client_socket.close()
        clients.remove(client_socket)
        broadcast(f"{client_names[client_socket]} has left the chat.".encode('utf-8'))

# 서버 시작
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))  # 서버 IP 및 포트 설정
    server_socket.listen(5)
    print("Server started on port 5555...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        clients.append(client_socket)

        # 각 클라이언트는 개별 스레드에서 처리
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
