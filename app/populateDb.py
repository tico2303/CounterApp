from models import *

user1 = User.query.filter_by(username="mathieu").first()

"""
user1 = User(username="juan", email="juan@gmail.com", password="juanPass")
user2 = User(username="john", email="john@gmail.com", password="johnPass")
user3 = User(username="Max",  email="Max@gmail.com", password="MaxPass")
user4 = User(username="Barby",email="Barby@gmail.com", password="BarbyPass")
# john is admin
team1 = Team(name="AwesomeGroup", admin=user2)
    # juan is admin
team2 = Team(name="Angels", admin=user1)
    # john is admin
team3 = Team(name="Dogers", admin=user2)
    # juan is admin
team4 = Team(name="CS171", admin=user1)
    # juans teams
member1 = Member(team=team1, membership=user1)
member2 = Member(team=team3, membership=user1)
member5 = Member(team=team2, membership=user1)
    # johns teams
member3 = Member(team=team1, membership=user2)
member4 = Member(team=team3, membership=user2)
member6 = Member(team=team2, membership=user2)
    # max teams
member7 = Member(team=team2, membership=user3)
    # Barby teams
member8 = Member(team=team2, membership=user4)

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(team1)
db.session.add(team2)
db.session.add(team3)
db.session.add(team4)
db.session.add(member1)
db.session.add(member2)
db.session.add(member3)
db.session.add(member4)
db.session.add(member5)
db.session.add(member6)
db.session.add(member7)
db.session.add(member8)

db.session.commit()
"""
