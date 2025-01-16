from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import NameOID
from cryptography import x509
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os

# Генерация RSA ключа
def generate_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

# Создание самоподписанного сертификата CA
def create_ca_certificate(ca_key):
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MyCA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "My CA")
    ])

    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )

    return ca_cert

# Создание серверного сертификата, подписанного CA
def create_server_certificate(server_key, ca_key, ca_cert):
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MyServer"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost")
    ])

    server_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )

    return server_cert

# Создание клиентского сертификата, подписанного CA
def create_client_certificate(client_key, ca_key, ca_cert):
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MyClient"),
        x509.NameAttribute(NameOID.COMMON_NAME, "client.local")
    ])

    client_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(client_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(private_key=ca_key, algorithm=hashes.SHA256())
    )

    return client_cert

# Сохранение ключей и сертификатов в файлы
def save_key_and_cert(key, cert, key_file, cert_file):
    with open(key_file, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(cert_file, "wb") as f:
        f.write(
            cert.public_bytes(encoding=serialization.Encoding.PEM)
        )

# Генерация ключа шифрования для Fernet
def generate_encryption_key(file_path):
    key = Fernet.generate_key()
    with open(file_path, "wb") as f:
        f.write(key)
    print(f"Ключ шифрования сохранен в {file_path}")

# Основной скрипт
if __name__ == "__main__":
    os.makedirs("certs", exist_ok=True)

    # Генерация ключа и сертификата CA
    ca_key = generate_key()
    ca_cert = create_ca_certificate(ca_key)
    save_key_and_cert(ca_key, ca_cert, "certs/ca_key.pem", "certs/ca_cert.pem")

    # Генерация ключа и сертификата для клиента
    client_key = generate_key()
    client_cert = create_client_certificate(client_key, ca_key, ca_cert)
    save_key_and_cert(client_key, client_cert, "certs/client_key.pem", "certs/client_cert.pem")
    print("Сертификаты и ключи для клиента сгенерированы и сохранены в папку 'certs'")

    # Генерация ключа и сертификата для сервера
    server_key = generate_key()
    server_cert = create_server_certificate(server_key, ca_key, ca_cert)
    save_key_and_cert(server_key, server_cert, "certs/server_key.pem", "certs/server_cert.pem")
    print("Сертификаты и ключи для сервера сгенерированы и сохранены в папку 'certs'")

    # Генерация ключа шифрования Fernet
    generate_encryption_key("certs/encryption_key.txt")
