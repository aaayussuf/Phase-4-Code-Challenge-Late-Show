from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lateshow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Routes

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{"id": e.id, "date": e.date, "number": e.number} for e in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": [
            {
                "id": a.id,
                "rating": a.rating,
                "guest_id": a.guest_id,
                "episode_id": a.episode_id,
                "guest": {
                    "id": a.guest.id,
                    "name": a.guest.name,
                    "occupation": a.guest.occupation
                }
            } for a in episode.appearances
        ]
    })

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{"id": g.id, "name": g.name, "occupation": g.occupation} for g in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.json
    try:
        new_appearance = Appearance(
            rating=data["rating"],
            episode_id=data["episode_id"],
            guest_id=data["guest_id"]
        )
        db.session.add(new_appearance)
        db.session.commit()

        return jsonify({
            "id": new_appearance.id,
            "rating": new_appearance.rating,
            "guest_id": new_appearance.guest_id,
            "episode_id": new_appearance.episode_id,
            "episode": {
                "id": new_appearance.episode.id,
                "date": new_appearance.episode.date,
                "number": new_appearance.episode.number
            },
            "guest": {
                "id": new_appearance.guest.id,
                "name": new_appearance.guest.name,
                "occupation": new_appearance.guest.occupation
            }
        }), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(debug=True)
