from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'rishal'
db = SQLAlchemy()
db.init_app(app)


# create table sponsor(id int, name varchar(100) NOT NULL, password varchar(100) UNIQUE)
class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

    campaigns = db.relationship('Campaign', lazy=True, backref='sponsor', cascade="all, delete-orphan")

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(100))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nam = request.form.get('username')
        pswd = request.form.get('password')
        # select * from sponsor where name = nam;
        sponsor = Sponsor.query.filter_by(name=nam).first()
        if sponsor:
            if sponsor.password == pswd:
                session['user_id'] = sponsor.id
                return redirect('/sponsordashboard')
            else:
                return "Wrong password"
        else:
            return "User not found"
        
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'] )
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        pas = request.form.get('password')
        sponsor = Sponsor(name=name, password=pas)
        db.session.add(sponsor)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/sponsordashboard')
def sponsordashboard():
    id = session['user_id']
    sponsor = Sponsor.query.filter_by(id=id).first()
    username = sponsor.name
    return render_template('sponsordashboard.html', sponsor_name=username)

@app.route('/create_campaign', methods=['POST'])
def create_campaign():
    if request.method == 'POST':
        name = request.form.get('campaign_name')
        niche = request.form.get('niche')
        sponsor_id = session['user_id']
        campaign = Campaign(name=name, niche=niche, sponsor_id=sponsor_id)
        db.session.add(campaign)
        db.session.commit()
        return redirect('/sponsordashboard')

if __name__ == '__main__':
    app.run(debug=True)