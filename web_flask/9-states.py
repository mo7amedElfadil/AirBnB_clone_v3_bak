#!/usr/bin/python3
"""
HBNB Flask web application server
App listens on 0.0.0.0 port 5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def close_storage(_=None):
    """
    Close storage
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    List all states
    """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    List all cities by states
    """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """
    List all states or state by id
    """
    states = storage.all(State)
    state = None
    if id:
        key = f"State.{id}"
        if key in states:
            state = states[key]
        else:
            states = None
    return render_template('9-states.html', states=states, state=state)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
