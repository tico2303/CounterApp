from app import app
from flask import render_template, redirect, url_for,request
from models import User, Team, Member,db
from forms import LoginForm, RegisterForm,NewTeamForm
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

################ Convience Methods for accessing DB #############################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DB convience function
def getUserTeams(uname):
    teamList = []
    user = User.query.filter_by(username=uname).first()
    for member in user.memberships.all():
        teamList.append(Team.query.filter_by(id=member.team_id).first().name)
    if len(teamList)==0:
        return ["No Teams"]
    return teamList

def getTeamMembers(teamName):
    membersList = []
    team = Team.query.filter_by(name=teamName).first()
    members = team.members.all()
    for member in members:
        membersList.append(User.query.filter_by(id=member.name_id).first().username)
    if len(membersList)== 0:
        return ["Is not a member to any teams"]
    return membersList	

#checks if team Name is taken
def isValidNewTeam(teamName):
    try:
        team = Team.query.filter_by(name=teamName).first()
        return False
    except IntegrityError:
        return True

# add functions to jinja enviornment so they are callable in html templates
app.jinja_env.globals.update(getUserTeams=getUserTeams)
app.jinja_env.globals.update(getTeamMembers=getTeamMembers)


################## Routes ##############################################
@app.route('/' )
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #return '<h1>' + form.username.data  + " " + form.password.data + "</h1>"
        #get first user in query because usernames are unique
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # checking password in db against what user entered in the form
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.password.data)
                return redirect(url_for('dashboard'))
        return "<h1>Invalid Username or Password</h1>"
    return render_template("login.html", form=form)


@app.route('/signup',methods=["GET","POST"])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return "<h1> New user has been created </h1>"
	return render_template("signup.html", form=form)

@app.route('/dashboard')
@login_required
def dashboard():
	user = User.query.filter_by(username=current_user.username).first()
	return render_template("dashboard.html", user=user)

@app.route('/search_teams', methods=["POST"])
@login_required
def search_teams():
    search_team  = request.form['search_team']
    user = User.query.filter_by(username=current_user.username).first()
    search_team_results = Team.query.filter_by(name=search_team).first()
    return render_template("search_teams.html", user=user, search_results = search_team_results)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/createteam',methods=["GET","POST"])
@login_required
def createteam():
    form = NewTeamForm()
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        print "teamName: ", form.teamname.data
        newTeam =Team(name=form.teamname.data, admin=user, code=form.teampassword.data)
        newMem = Member(team=newTeam,membership=user)
        db.session.add(newTeam)
        db.session.add(newMem)
        db.session.commit() 
        return redirect(url_for('teamcreated'))
    return render_template("CreateTeam.html", user=user, form=form)

@app.route('/vote',methods=["GET","POST"])
@login_required
def vote():
    teamname = request.form["teamname"]
    team = Team.query.filter_by(name=teamname).first()
    user = User.query.filter_by(username=current_user.username).first()
    return render_template("Vote.html", team=team,user=user )

@app.route('/teamcreated', methods=["GET"])
@login_required
def teamcreated():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template("TeamCreated.html", user=user)

@app.route('/teamview',methods=["POST"])
@login_required
def teamview():
    team = request.form["teamname"]
    return render_template("Teamview.html", team=team )


