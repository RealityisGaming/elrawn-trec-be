from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import psycopg2
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ixpwwytxodzuvu:b3113760a23d52e0ce67f38e0eb1a6a1de6a9e03f8047e52e07be33446c0eb03@ec2-52-3-60-53.compute-1.amazonaws.com:5432/dace9o62ldnod1"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app, resources={r'/*': {'origins': '*'}})

# class Enemy(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     named = db.Column(db.String(52), nullable= False)
#     family = db.Column(db.String, nullable= False)
#     damage = db.Column(db.Integer, nullable= False)
#     skills = db.Column(db.String, nullable= False)
#     skills_two = db.Column(db.String, nullable= False)
#     skills_three = db.Column(db.String, nullable= False)

#     def __init__(self, named, family, damage, skills, skills_two, skills_three):
#         self.named = named
#         self.family = family
#         self.damage = damage
#         self.skills = skills
#         self.skills_two = skills_two
#         self.skills_three = skills_three

# class EnemySchema(ma.Schema):
#     class Meta:
#         fields = ("id","named","family","damage","skills","skills_two","skills_three")

# enemy_schema = EnemySchema()
# enemies_schema = EnemySchema(many = True)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(16), unique= True, nullable = False)
    job = db.Column(db.String, nullable = False)
    level = db.Column(db.Integer, default = 1)
    xp = db.Column(db.Integer, default = 0)
    skill = db.Column(db.String, nullable = False)
    skill_two = db.Column(db.String, nullable = False)
    skill_three = db.Column(db.String, nullable = False)

    def __init__(self, name, job, skill, skill_two, skill_three):
        self.name = name
        self.job = job
        self.skill = skill
        self.skill_two = skill_two
        self.skill_three = skill_three

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "job", "level", "xp","skill", "skill_two", "skill_three")

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)




@app.route("/")
def homepage():
    return "string"

@app.route("/battles")
def attack_time():
    enemies = db.session.query(Enemy().all)

    return jsonify(enemies_schema.dump(enemies))

# @app.route("/enemy", methods = ["POST"])
# def enemies():
#     enemy_data = request.get_json()
#     named = enemy_data.get("named")
#     family = enemy_data.get("family")
#     damage = enemy_data.get("damage")
#     skills = enemy_data.get("skills")
#     skills_two = enemy_data.get("skills_two")
#     skills_three = enemy_data.get("skills_three")

#     new_enemy = Enemy(named, family, damage, skills, skills_two, skills_three)
#     db.session.add(new_enemy)
#     db.session.commit()
#     return enemy_schema.jsonify(new_enemy)

@app.route("/characters")
def get_over_here():
    characters = db.session.query(Character).all()

    return jsonify(characters_schema.dump(characters))

@app.route("/character", methods = ["POST"])
def just_pick_one():
    character_data = request.get_json()
    name = character_data.get("name")
    job = character_data.get("job")
    skill = character_data.get("skill")
    skill_two = character_data.get("skill_two")
    skill_three = character_data.get("skill_three")

    new_character = Character(name, job, skill, skill_two, skill_three)
    db.session.add(new_character)
    db.session.commit()
    return character_schema.jsonify(new_character)

@app.route("/character/<id>", methods = ["DELETE"])
def remove_me(id):
    character_to_delete = db.session.query(Character).filter(Character.id == id).first()
    db.session.delete(character_to_delete)
    db.session.commit()
    return jsonify("Your character has been deleted")


       


if __name__ == "__main__":
    app.run(debug = True)