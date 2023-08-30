from flask import Flask, jsonify
from model import Habitacion
import threading
import time

app = Flask(__name__)

# Create an instance of your model
model = Habitacion(M=20, N=20)  # Adjust the parameters as needed

def send_positions():
    positions = []
    for robot in model.robos:
        positions.append({
            "id": robot.unique_id,
            "position": robot.pos,
            "charge": robot.carga,
            "charging": robot.cargando
        })
    return positions

def simulate_and_send():
    while True:
        model.step()
        positions = send_positions()
        with app.app_context():
            app.response_class(
                response=jsonify(positions),
                status=200,
                mimetype='application/json'
            )
        time.sleep(1)

@app.route('/positions')
def get_positions():
    positions = send_positions()
    return jsonify(positions)

if __name__ == '__main__':
    simulation_thread = threading.Thread(target=simulate_and_send)
    simulation_thread.start()

    app.run(debug=True)