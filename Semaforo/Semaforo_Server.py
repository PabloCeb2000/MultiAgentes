from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit, time
from Semaforo_script_I import SemaforoModel

app = Flask(__name__, static_url_path='')

# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

model = SemaforoModel(24, 24)
all_positions = []

@app.route('/')
def root():
    return [{"message":"Hello World"}]

@app.route('/run_simulation')
def run_simulation():

   
    model.step()
    #all_positions.append(model.get_agent_positions())
    positions = {
        "agentes": model.get_agent_position(),
    }
    return json.dumps(positions)

@app.route('/run_simulation_Sem')
def run_simulation_Sem():

   
    model.step()
    positions = {
        "semaforos": model.get_agent_position_Sem()
    }
    return json.dumps(positions)


@app.route('/agent')
def agent():

    response = app.response_class(
        response=json.dumps({"x":20,"y":40}),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)