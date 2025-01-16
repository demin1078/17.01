from flask import Flask, request, jsonify

app = Flask(__name__)

@app.before_request
def verify_client_cert():
    cert = request.get_json().get('certificate', None)
    if not cert:
        return jsonify({"error": "Certificate missing"}), 400
    # Логика для проверки сертификатов можно добавить здесь, если нужно
    return None  # Пропустим проверку для тестирования

@app.route('/api/data', methods=['POST'])
def get_data():
    data = request.get_json().get('data', '')
    if not data:
        return jsonify({"error": "Data missing"}), 400
    # Обработка данных, просто возвращаем их для демонстрации
    return jsonify({'result': 'ok', 'received_data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Запуск сервера без SSL
