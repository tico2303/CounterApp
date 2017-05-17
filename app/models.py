from app import db
from flask_login import UserMixin

################### Database ORM(Object Relational Models) #############
class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	memberships = db.relationship("Member", backref="membership", lazy="dynamic")

class Team(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))
	members = db.relationship("Member", backref="team", lazy="dynamic")	

class Member(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

