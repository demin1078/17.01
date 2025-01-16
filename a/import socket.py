import socket
import struct
import time

# Настройки Multicast
MCAST_GRP = "224.1.1.1"  # Multicast адрес
MCAST_PORT = 5007        # Порт для отправки сообщений
TTL = 1                  # Время жизни пакета (1 означает только в локальной сети)

# Создаем сокет для отправки данных через UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Настраиваем TTL (Time-To-Live) пакета
ttl = struct.pack('b', TTL)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


message = "Привет, Multicast группа!"
# Отправляем сообщение в Multicast группу
sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
print(f"Отправлено сообщение: {message}")
time.sleep(2)  # Отправляем сообщение каждые 2 секунды
