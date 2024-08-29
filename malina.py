from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/process_order', methods=['POST'])
def process_order_route():
    print(request)
    data = request.json
    order_id = data.get('order_id')
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    product_category = data.get('product_category')
    seat_id = data.get('seat_id')
    print(order_id, product_id, product_name, product_category, seat_id)
    return jsonify({"status": "Order processed successfully"}), 200


@app.route('/start_talking', methods=['GET'])
def start_talking_route():
    print("Switch to start talk!")
    return jsonify({"status": "Started talking"}), 200


@app.route('/stop_talking', methods=['GET'])
def stop_talking_route():
    print("Switch to stop talk!")
    return jsonify({"status": "Stopped talking"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
