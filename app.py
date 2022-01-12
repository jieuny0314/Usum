from flask import Flask, render_template, request, redirect, url_for, session, g, abort, Response, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from sqlalchemy import and_, or_
import nhRequests, utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LEEHAHOON'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean' 
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test!@#'
#app.config['BASIC_AUTH_FORCE'] = True

db = SQLAlchemy(app)
basic_auth = BasicAuth(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	accname = db.Column(db.String(10), nullable=False)
	banktype = db.Column(db.String(5), nullable=False)
	birthday = db.Column(db.DateTime, nullable=False)
	cardnum = db.Column(db.String(40), nullable=False)
	accnum = db.Column(db.String(40), nullable=False)
	Fincard = db.Column(db.String(40), nullable=True)
	connCode = db.Column(db.String(15), nullable=True)
	
class TransHistory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	connCode = db.Column(db.String(15), nullable=True)
	username = db.Column(db.String(100))
	Trdd = db.Column(db.DateTime)
	Usam = db.Column(db.String(100))
	AfstNm = db.Column(db.String(100))
	Category = db.Column(db.String(100), nullable=True)
	CardAthzNo = db.Column(db.String(50))

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class MyModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


admin = Admin(app, name='microblog', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(ModelView(User, db.session)) 
admin.add_view(ModelView(TransHistory, db.session))

@app.before_request
def before_request():
    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).one()
    else:
        g.user = None

@basic_auth.required
class AdminView(ModelView):
  pass

@app.route('/')
def index():
	user = None
	if 'user_id' in session:
		user_id = session['user_id']
		user = User.query.filter_by(id=user_id).one()

	if user != None:
		return render_template('html/user.html', user=user)

	else:
		return render_template('html/main.html')

@app.route('/signup')
def signup_form():
	return render_template('html/signup.html')

@app.route('/signup', methods=['POST'])
def signup():
	user = User()
	user.username = request.form['username']
	user.accname = request.form['accname']
	user.password = generate_password_hash(request.form['password'])
	user.banktype = utils.BankType[request.form['bankName']]
	user.cardnum = request.form['cardnumber']
	user.accnum = request.form['account']
	user.birthday = utils.str2datetime(request.form['birth-year']+request.form['birth-month']+\
		request.form['birth-day'])
	#fincard = nhRequests.getFinCard(user.birthday, user.cardnum)
	user.Fincard = nhRequests.TestFincard
	db.session.add(user)
	db.session.commit()
	print('***',request.form)
	return redirect('/')

@app.route('/users/<int:user_id>/couplecode')
def getCoupleCode(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	code = utils.makeCode()
	user.connCode = code
	db.session.commit()
	return render_template('html/couplecode.html', code=code, user=user)

@app.route('/users/<int:user_id>/setcode')
def setCodeForm(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	return render_template('html/inputcode.html', user=user)

@app.route('/users/<int:user_id>/setcode', methods=['POST'])
def setCoupleCode(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	user.connCode = request.form['code']
	db.session.commit()
	return redirect('/')

@app.route('/users/<int:user_id>/datecheck')
def userAccount(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	cardHistory = nhRequests.getCardUseHistory(True)
	return render_template('html/checklist.html', user=user, cardHis=cardHistory)

@app.route('/users/<int:user_id>/datecheck', methods=['POST'])
def setTransHis(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	cardHistory = nhRequests.getCardUseHistory(True)
	for hisList in cardHistory['REC']:
		for userInput in request.form:
			if userInput in hisList['CardAthzNo']:
				trans = TransHistory()
				trans.Trdd = utils.str2datetime(hisList['Trdd'])
				trans.Usam = hisList['Usam']
				trans.AfstNm = hisList['AfstNm']
				trans.username = user.username
				trans.connCode = user.connCode
				trans.CardAthzNo = hisList['CardAthzNo']
				db.session.add(trans)
				db.session.commit()

	return redirect('/users/'+str(user.id)+'/get_category')

@app.route('/users/<int:user_id>/get_category')
def getCategory(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)
	his = TransHistory.query.filter(and_(TransHistory.connCode==user.connCode, \
		TransHistory.username==user.username)).order_by(TransHistory.Trdd).all()
	return render_template('html/setcategory.html', user=user, his=his)

@app.route('/users/<int:user_id>/get_category', methods=['POST'])
def setCategory(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)
	
	print("***", request.form)
	for userInput in request.form:
		trans = TransHistory.query.filter_by(CardAthzNo=userInput).first()
		trans.Category = request.form[userInput]
		print('*()',request.form[userInput])
		db.session.commit()
	
	return redirect('/')


@app.route('/users/<int:user_id>/result')
def showResult(user_id):
	user = User.query.filter_by(id=user_id).first()
	his = TransHistory.query.filter_by(connCode=user.connCode).order_by(TransHistory.Trdd).all()
	return render_template('result.html', user=user, his=his)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		print(request.form)
		user = User.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = '아이디 또는 비밀번호가 잘못되었습니다.'
		elif not check_password_hash(user.password, request.form['password']):
			error = '아이디 또는 비밀번호가 잘못되었습니다.'
		else:
			session['user_id'] = user.id
			return redirect(url_for('index'))

	return render_template('html/login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/users/<int:user_id>/daylist')
def daylist(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	his = TransHistory.query.filter_by(connCode=user.connCode).all()

	return render_template('html/daylist.html', user=user, his=his, mon=1, total=0)

@app.route('/users/<int:user_id>/daylist', methods=['POST'])
def daylistPost(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	his = TransHistory.query.filter_by(connCode=user.connCode).all()
	total = utils.getCoupleTotal(user.connCode, request.form['month-list'])
	return render_template('html/daylist.html', user=user, his=his, mon=request.form['month-list'], \
		total=total)

@app.route('/users/<int:user_id>/catelist')
def catelist(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	a_total = utils.getCoupleTotal(user.connCode, '12')
	res = dict()
	print("^^^",utils.getCateTotal('음식점'), a_total)
	res['음식점'] = utils.Total2Percent(utils.getCateTotal('음식점'), a_total)
	res['카페'] = utils.Total2Percent(utils.getCateTotal('카페'), a_total)
	res['교통'] = utils.Total2Percent(utils.getCateTotal('교통'), a_total)
	res['놀거리'] = utils.Total2Percent(utils.getCateTotal('놀거리'), a_total)
	res['편의점'] = utils.Total2Percent(utils.getCateTotal('편의점'), a_total)
	res['패션'] = utils.Total2Percent(utils.getCateTotal('패션'), a_total)
	res['생필품'] = utils.Total2Percent(utils.getCateTotal('생필품'), a_total)
	res['기타'] = utils.Total2Percent(utils.getCateTotal('기타'), a_total)

	return render_template('html/categorylist.html', res=res)


@app.route('/users/<int:user_id>/dutchpay')
def dutchpay(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	couple_total = utils.getCoupleTotal(user.connCode, '20201203')
	user_total = utils.getUserTotal(user.username, '20201203')
	dutch = int(couple_total/2)
	partner = User.query.filter(and_(User.connCode==user.connCode, \
		User.username!=user.username)).first()

	for key, value in utils.BankType.items():
		if value == partner.banktype:
			p_banktype=key

	return render_template('html/dutchpay.html', user=user, c_total=couple_total, u_total=user_total,\
		dutch=dutch, partner=partner, p_banktype=p_banktype)

@app.route('/users/<int:user_id>/sendpay', methods=['GET'])
def sendpay(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	if not session:
		return abort(403)

	partner = User.query.filter(and_(User.connCode==user.connCode, \
		User.username!=user.username)).first()
	print(request.args.get('cost'))
	nhRequests.Trans2Usum(nhRequests.TestFinaccount, request.args.get('cost'), '어썸-더치페이', 'test')

	nhRequests.send2accNum(partner.banktype, partner.accnum, request.args.get('cost'),\
		partner.accname, "어썸-더치페이")

	return "<script>window.onload = window.close();</script>"

@app.route('/users/<int:user_id>/coupleratio')
def coupleratio(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	if not session:
		return abort(403)


	partner = User.query.filter(and_(User.connCode==user.connCode, \
		User.username!=user.username)).first()

	myTotal = utils.getUserTotal(user.username, '12')
	paTotal = utils.getUserTotal(partner.username, '12')
	a_total = myTotal+paTotal
	myPerct = utils.Total2Percent(myTotal, a_total)
	paPerct = utils.Total2Percent(paTotal, a_total)
	return render_template('html/coupleratio.html', user=user, partner=partner, \
		myTotal=myTotal, paTotal=paTotal, myPerct=myPerct, paPerct=paPerct)


@app.route('/users/<int:user_id>/product')
def product(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return abort(404)

	if not session:
		return abort(403)

	return render_template('html/recommend.html')

if __name__=='__main__':
	app.run(debug=False, host='0.0.0.0')
