from services.hint_bundler import bundle_hints
from utils.country_randomiser import random_countries
from services.game_instance_builder import GameInstance, HardGameInstance
import flask
import os

secret_key = os.urandom(16).hex()

app = flask.Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/game')
def game():
    game_instance = get_session_data()
    
    if game_instance is None:
        return flask.redirect(flask.url_for('index'))

    if game_instance.rounds_played > 5:
        return flask.redirect(flask.url_for('end_game'))
    return flask.render_template('game.html', game_instance=game_instance)

@app.route('/game/next-hint', methods=['POST'])
def next_hint():
    game_instance = get_session_data()
    
    if game_instance is None:
        return flask.redirect(flask.url_for('game'))

    game_instance.show_next_hint()

    flask.session['game_instance'] = game_instance.to_dict()
    return flask.redirect(flask.url_for('game'))

@app.route('/game/guess', methods=['POST'])
def guess():
    game_instance = get_session_data()
    
    if game_instance is None:
        return flask.redirect(flask.url_for('game'))

    guess = flask.request.form['guess']
    game_instance.guess(guess)
    flask.session['game_instance'] = game_instance.to_dict()
    return flask.redirect(flask.url_for('game'))

@app.route('/game/end')
def end_game():
    game_instance = get_session_data()
    
    if game_instance is None:
        return flask.redirect(flask.url_for('game'))

    return flask.render_template('end.html', game_instance=game_instance)

@app.route('/game/new')
def new_game():
    game_instance = GameInstance()
    game_instance.new_game()
    flask.session['game_instance'] = game_instance.to_dict()

    return flask.redirect(flask.url_for('game'))

@app.route('/game/new/hard')
def new_hard_game():
    game_instance = HardGameInstance()
    game_instance.new_game()
    flask.session['game_instance'] = game_instance.to_dict()

    return flask.redirect(flask.url_for('game'))


def get_session_data():
    data = flask.session.get('game_instance')
    if data:
        if data.get('difficulty') == 'hard':
            return HardGameInstance.from_dict(data)
        else:
            return GameInstance.from_dict(data)
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)

