from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from sqlalchemy import update

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///userdb.db'
db = SQLAlchemy(app)


################### Database ORM(Object Relational Models) #############
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))
	memberships = db.relationship("Member", backref="membership", lazy="dynamic")
        admin_team =  db.relationship("Team", backref="admin", lazy="dynamic")

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
	

##################### Convience Functions ################################

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
                vote = int(raw_input())
                if vote ==1:
                        print "before update: "
                        mem = Member.query.filter_by(name_id=user.id).first()
                        print "count: ",mem.count
                        print "after update: "
                        if mem.count == None:
                                mem.count = 1
                        else:
                                mem.count = mem.count +1
                        db.session.commit()
                        mem_new = Member.query.filter_by(name_id=user.id).first()
                        print "count: ", mem_new.count
                        team = Team.query.filter_by(name=teamName).first()
                        members = team.members.all()
                        sum = 0
                        for member in members:
				print "member: ", member
				print "member: ", User.query.filter_by(id=member.name_id).first().username
				print "member.count: ", member.count
                                if member.count !=None:
                                        sum += member.count
                        print "sum: ", sum
                        teamMenu(teamName, user)

        else:
                print "YOUR NOT A MEMBER OF ", teamName
        



def isMember(teamName, uname):
        teamList = getUserTeams(uname)
        if teamName in teamList:
                return True
        else:
                return False	

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



""" 
def groups_menu():
        print "GROUP MENU"
        print "1.See all Groups(Teams)"
        print "2.Create New Team"
        print "3.Edit Existing Team"        
        resp = int(raw_input())
        if resp == 1:
                teams = Team.query.all()
                print "Teams are: "
                for i, team in enumerate(teams):
                        print"\t",i,": ",team.name
        if resp == 2:
                create_team_menu()
        if resp == 3:
                edit_team_menu()


def create_team_menu():
        print "CREATE A NEW TEAM MENU"          
        print "Enter name of team: "
        tname = raw_input() 
        resp = 0
        while resp !=2:
                print "Now choose members"
                print "1. List of Users"
                print "2. Add a member my name"      
                resp = int(raw_input())
                if resp == 1:
                        u = User.query.all()
                        for user in u:
                                print user.username
                        print "\n"
                elif resp == 2:
                        print "Enter members name to add to ", tname
                        member = raw_input()
                        user = [User.query.filter_by(username=member).first()]
                        
                        createTeam(tname, user) 
        

def edit_team_menu():
        print "EDIT TEAM MENU"
        print "Enter name of team to edit"
        tname = raw_input()
                         

def users_menu():
        print "1. See all users"
        resp = int(raw_input())
        if resp == 1:
                users = User.query.all()
                print "Choose a user"
                for i, user in enumerate(users):
                        print i,". ",user.username
                choice = int(raw_input())
                
                #Specific User stats 
                user = users[choice]                
                print "username: ", user.username
                teamlist = getUserTeams(user.username)
                print "teams: ",[i for i in teamlist]                 
                print "team mates: "
                for i in teamlist:
                        print "\t", i, ": ",getTeamMembers(i)
"""
def countTestMenu():
       # view user Teams
       # inc count for user in team
       # when Done return total and percentages  
        print "User to Team status:\n"
        u = User.query.all()
        for i, user in enumerate(u):
                print i, ". ", user.username
                print "\t", getUserTeams(user.username)
                print "\n"
        print "\n\n" 

def viewTeam(): 
        print "choose Team/room to enter: "
        t = Team.query.all()
        for i, team in enumerate(t): 
                print i, ". ", team.name
        print "\n\n"          
        team = raw_input()
        tm = Team.query.filter_by(name=team)
        return tm
           
        



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
	
	user = User.query.filter_by(username="juan").first()
	teamName = "Angels"
	###### inc vote
	
	angels = Team.query.filter_by(name=teamName).first()
	
	#members list	
		
		
			
	# get sum


if __name__ == '__main__':

	#Create users			
	"""
	print(" juans teams are: ")
	getUserTeams("juan")
	print("\n")
	print("Members of the Angels team are: ")
	getTeamMembers("Angels")
        team = Team(name=tname) 
	"""
        #menu()

       	testVote() 


        """
	user1 = User(username="juan", email="juan@gmail.com", password="juanPass")
	user2 = User(username="john", email="john@gmail.com", password="johnPass")
	user3 = User(username="Max",  email="Max@gmail.com", password="MaxPass")
	user4 = User(username="Barby",email="Barby@gmail.com", password="BarbyPass")
        
        #john is admin
	team1 = Team(name="AwesomeGroup", admin=user2)
        #juan is admin
	team2 = Team(name="Angels", admin=user1)
        #john is admin
	team3 = Team(name="Dogers", admin=user2)
        #juan is admin
	team4 = Team(name="CS171", admin=user1)
        
        #juans teams
	member1 = Member(team=team1, membership=user1)
	member2 = Member(team=team3, membership=user1)
	member5 = Member(team=team2, membership=user1)
        #johns teams
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
	#get user info	
	#user2 = User.query.filter_by(username="juan").first()
	#user3 = User.query.filter_by(username="john").first()
	#user4 = User.query.filter_by(username="Max").first()
	
