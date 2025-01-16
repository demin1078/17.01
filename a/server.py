from flask import Flask, request, jsonify
import ssl
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

app = Flask(__name__)

@app.before_request
def verify_client_cert():
    cert = request.get_json().get('certificate')
    if not cert:
        return jsonify({"error": "Certificate missing"}), 400
    # Verify certificate against CA
    if not verify_certificate(cert):
        return jsonify({"error": "Invalid certificate"}), 401

@app.route('/api/data', methods=['POST'])
def get_data():
    data = request.get_json().get('data')
    if not data:
        return jsonify({"error": "Data missing"}), 400
    # Decrypt data
    decrypted_data = decrypt_data(data)
    # Process decrypted data
    return jsonify({'result': 'ok', 'received_data': decrypted_data})

def verify_certificate(cert_pem):
    # Load certificate
    certificate = load_pem_x509_certificate(cert_pem.encode(), default_backend())
    # Verify certificate against CA
    try:
        certificate.public_key().verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Certificate verification failed: {e}")
        return False

def decrypt_data(encrypted_data):
    # Load encryption key
    try:
        key = open('certs/encryption_key.txt', 'rb').read()
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data.encode())
        return decrypted_data.decode()  # Assuming the data is UTF-8 encoded
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

if __name__ == '__main__':
    # Create SSL context for secure communication
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('certs/server_cert.pem', 'certs/server_key.pem')
    context.load_verify_locations('certs/ca_cert.pem')
    context.verify_mode = ssl.CERT_REQUIRED  # Ensure the client certificate is verified
    
    app.run(host='0.0.0.0', port=8000, ssl_context=context)  # Run with SSL



# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Убираем проверку сертификатов для упрощения тестирования
# @app.before_request
# def verify_client_cert():
#     cert = request.get_json()#.get('certificate')
#     if not cert:
#         return jsonify({"error": "Certificate missing"}), 400
#     # Проверка сертификата оставлена для примера, но в этом случае она будет всегда пропускаться
#    # if not verify_certificate(cert):
#      #   return jsonify({"error": "Invalid certificate"}), 401

# @app.route('/api/data', methods=['POST'])
# def get_data():
#     # Получаем данные из тела запроса
#     data = request.get_json().get('data')
#     if not data:
#         return jsonify({"error": "Data missing"}), 400
#     # Здесь можно добавить обработку данных
#     return jsonify({'result': 'ok', 'received_data': data})

# # Проверка сертификата (опционально, если нужно)
# def verify_certificate(cert_pem):
#     # Здесь можно добавить проверку сертификата, если он передается в запросе
#     # На данный момент эта функция просто возвращает True, для упрощения.
#     return True

# def decrypt_data(encrypted_data):
#     # Если необходимо расшифровать данные, добавьте этот код
#     # Здесь пока оставим заготовку для дальнейшего использования
#     pass

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)  # Запуск сервера на порту 8000 без SSL
