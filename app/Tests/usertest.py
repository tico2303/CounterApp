from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from sqlalchemy import update

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///userdb.db'
db = SQLAlchemy(app)


# Database ORM(Object Relational Models) #############
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    memberships = db.relationship("Member", backref="membership", lazy="dynamic")
    admin_team =db.relationship("Team", backref="admin", lazy="dynamic")

class Team(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    members = db.relationship("Member", backref="team", lazy="dynamic")    

class Member(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    count = db.Column(db.Integer)

# Convience Functions ################################


################ MENU ##############################3
def menu():
    print "1.Login"
    print "2.Sign Up"
    resp = int(raw_input())
    if resp == 1:
        user = login()
    elif resp == 2:
        user = signup()
    if user:
        dashmenu(user)       

def login():
    print "enter username"
    uname = raw_input()
    print "enter password"
    passwd = raw_input()
    try:
            u = User.query.filter_by(username=uname).first()
            if u.password == passwd:
                    print "login Succesfull"
                    return u
    except:
            print "Username: ", uname, " not found"
            login()

def dashmenu(user):
        print "1.View teams"
        print "2.Join team"
        print "3.create team"
        resp = int(raw_input())
        if resp == 1:
                print getUserTeams(user.username) 
                dashmenu(user)
        elif resp == 2:
                print "Choose Team Name to join: "
                print getUserTeams(user.username) 
                teamName = raw_input()
                teamMenu(teamName,user)
        elif resp == 3:
                print "create Team...implement"  


def teamMenu(teamName, user):
        if isMember(teamName, user.username):
                print "Your a member of ", teamName
                print "1. Yes vote"
                print "2. No vote"
                print "3. back"
                print "4. reset count"
                print "5. View Vote Stats"
                print "6. View all members of the ", teamName
                print "7. Clear all votes"
                vote = int(raw_input())
                team = Team.query.filter_by(name=teamName).first()
                #Vote Yes
                if vote ==1:
                        incCountUnique(team,user)
                        print user.username, " current count: ",getUserCount(team,user)
                        total_count, num_voters = getTotalCount(team)
                        print "Teams Total count:", total_count
                        print "Percentage: ", (float(total_count)/float(num_voters))*100
                        teamMenu(teamName, user)
                #Vote No
                elif vote == 2:
                    setCount(team,user,0)
                    print user.username, " current count: ",getUserCount(team,user)
                    total_count, num_voters = getTotalCount(team)
                    print "Teams Total count:", total_count
                    print "Percentage: ", (float(total_count)/float(num_voters))*100
                    teamMenu(team.name,user)
                #Go Back
                elif vote == 3:
                    dashmenu(user)
                #Reset Count
                elif vote == 4:
                    setCount(team,user,0)
                    teamMenu(team.name,user)
                #View Vote Stats
                elif vote == 5:
                    total_count, num_voters = getTotalCount(team)
                    print "Teams Total count:", total_count
                    print "Percentage: ", (float(total_count)/float(num_voters))*100
                    teamMenu(teamName, user)
                #View all members
                elif vote == 6:
                    print "implement see all users"
                    print getAllMembers(team)
                    teamMenu(teamName, user)
                elif vote == 7:
                    clearAllVotes(team,user)
                    teamMenu(teamName,user)
        else:
                print "YOUR NOT A MEMBER OF ", teamName

################ END MENU #############################


############### Core Functions ########################
def getAllMembers(team):
    memberList = []
    members = team.members.all()
    for member in members:
        user = User.query.filter_by(id=member.name_id).first().username
        memberList.append(user)
    return memberList

def isAdmin(team, user):
    if team.admin.id == user.id:
        return True
    return False

def isMember(teamName, uname):
        teamList = getUserTeams(uname)
        if teamName in teamList:
                return True
        else:
                return False    
def clearAllVotes(team, user):
    if isAdmin(team,user):
        print user.username, " is Admin!"
        print "memebers: "
        for member in team.members:
            print "member.id",member.id
            member.count = 0
        db.session.commit()

def getUserTeams(uname):
    teamList = []
    user = User.query.filter_by(username=uname).first()
    for member in user.memberships.all():
        teamList.append(Team.query.filter_by(id=member.team_id).first().name)
    return teamList

def getTeamMembers(teamName):
    membersList = []
    team = Team.query.filter_by(name=teamName).first()
    members = team.members.all()
    for member in members:
        membersList.append(User.query.filter_by(id=member.name_id).first().username)
    return membersList

def createTeam(teamName, users=None):
        team = Team(name=teamName)
        if users==None:
                db.session.add(team)
        else:
            for user in users:
                m = Member(team=team,membership=user)
                db.session.add(m)
        db.session.commit()

def addMemberToTeam(teamid,user):
        team = Team.query.filter_by(id=teamid).first()


################ Count Functions ################
def incCount(team, user):
    member = Member.query.filter_by(team_id=team.id, name_id=user.id).first()
    if member.count == None:
        member.count = 1
    else:
        member.count +=1
    db.session.commit()

def incCountUnique(team,user):
    member = Member.query.filter_by(team_id=team.id, name_id=user.id).first()
    if member.count == None or member.count==0:
        member.count = 1
        db.session.commit()
    elif member.count == 1:
        pass
def setCount(team,user,value):
    member = Member.query.filter_by(team_id=team.id, name_id=user.id).first()
    member.count = value
    db.session.commit()

def resetCount(team,user):
    setCount(team,user,None)
    db.session.commit()

#for debugging
def getUserCount(team, user):
    mems = user.memberships.filter_by(team_id=team.id).all()
    for m in mems:
        print m.count

def getTotalCount(team):
    total = 0
    numOfVoters = 0
    for member in team.members.all():
        if member.count !=None:
            total +=member.count 
            numOfVoters +=1
    return total, numOfVoters

###### END Count Functions ################


def testVote():
    print "MEMBERS TABLE"
    m = Member.query.all()
    for mem in m:
        print "id: ", mem.id
        print "name_id: ", mem.name_id
        print "team_id: ", mem.team_id
    print "\n\n"
    print "USER TABLE"
    u = User.query.all()
    for user in u:
        print "id: ", user.id
        print "username: ", user.username
        print "memberships: " 
        for membership in user.memberships.all():
            print "\t    id: ", membership.id
            print "\t    team_id: ", membership.team_id
            print "\t    name_id: ", membership.name_id
            print "\t count: ", membership.count
        print "\n"
    print "\n\n"
    juan = User.query.filter_by(username="juan").first()
    john = User.query.filter_by(username="john").first()
    teamName = "Angels"
    # inc vote
    angels = Team.query.filter_by(name=teamName).first()

    print "is juan Admin of angels?", isAdmin(angels,juan) 
    print "Is john Admin of angels?", isAdmin(angels,john)
    print "current total: ", getTotalCount(angels) 
    print "juans total count:",getUserCount(angels,juan)
    print "incrementing juans count:", incCount(angels, juan)
    print "updated toal: ", getTotalCount(angels)
    print "juans total count:",getUserCount(angels,juan)
    print "Getting all members of", angels.name
    angels = Team.query.filter_by(name=teamName).first()
    print getAllMembers(angels)
    #db.session.commit()
    # members list
    # get sum


if __name__ == '__main__':

    # Create users
    """
    print(" juans teams are: ")
    getUserTeams("juan")
    print("\n")
    print("Members of the Angels team are: ")
    getTeamMembers("Angels")
        team = Team(name=tname) 
    """
    menu()
    #testVote() 

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
    # get user info    
    # user2 = User.query.filter_by(username="juan").first()
    # user3 = User.query.filter_by(username="john").first()
    # user4 = User.query.filter_by(username="Max").first()

