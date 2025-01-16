import socket
import struct

# Настройки Multicast
MCAST_GRP = "224.1.1.1"  # Multicast адрес
MCAST_PORT = 5007        # Порт для получения сообщений

# Создаем сокет для получения данных через UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Привязываем сокет к любому локальному адресу и указанному порту
sock.bind(('', MCAST_PORT))

# Настраиваем подписку на Multicast группу
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Ожидание сообщений от Multicast группы...")

try:
    while True:
        # Получаем сообщение
        data, addr = sock.recvfrom(1024)  # Размер буфера 1024 байта
        print(f"Сообщение от {addr}: {data.decode()}")
except KeyboardInterrupt:
    print("\nПрием сообщений остановлен.")
    sock.close()
