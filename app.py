from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from login_manager import login_manager
from controllers import setup_routes

app = Flask(__name__)

# DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/my_memo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

#db = SQLAlchemy(app)


# Flask_Login 설정
# login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # 로그인 페이지의 뷰 함수 이름

setup_routes(app)   # 라우팅 설정

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

# 데이터 모델 정의
# class Memo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # 사용자 참조 추가
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.String(1000), nullable=False)

#     def __repr__(self):
#         return f'<Memo {self.title}>'
    
# # 유저 데이터 모델
# class User(UserMixin, db.Model):
#     # __tablename__ = 'Users' 
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(512))

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    


# # 기존 라우트
# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/about')
# def about():
#     return '이것은 마이 메모 앱의 소개 페이지입니다.'

# DB 생성
# with app.app_context():
#     db.create_all()

# jsonify() 함수로 파이썬 데이터 구조를 JSON 형식으로 변환
# 이를 클라이언트 응답으로 보내는데 사용    

# # 메모 생성
# @app.route('/memos/create', methods=['POST'])
# @login_required
# def create_memo():
#     title = request.json['title']
#     content = request.json['content']
#     # new_memo = Memo(title=title, content=content)
#     new_memo = Memo(user_id=current_user.id, title=title, content=content)
#         # 헤당 메모가 어떤 사용자에 의해 작성된건지 식별 가능
#     db.session.add(new_memo)
#     db.session.commit()

#     return jsonify({'message': 'Memo created'}), 201


# # 메모 조회
# @app.route('/memos', methods=['GET'])
# @login_required
# def list_memos():
#     # memos = Memo.query.all()
#     #return jsonify([{'id': memo.id, 'title': memo.title, 'content': memo.content} for memo in memos]), 200
#     memos = Memo.query.filter_by(user_id=current_user.id).all()
#     return render_template('memos.html', memos=memos, username=current_user.username)


# # 메모 업데이트
# @app.route('/memos/update/<int:id>', methods=['PUT'])
# @login_required
# def update_memo(id):
#     # memo = Memo.query.filter_by(id=id).first()
#     memo = Memo.query.filter_by(id=id, user_id=current_user.id).first() # 현재 사용자의 메모만 선택

#     if memo:
#         memo.title = request.json['title']
#         memo.content = request.json['content']
#         db.session.commit()
#         return jsonify({'message': 'Memo updated'}), 200
    
#     else:
#         abort(404, description="Memo not found or authorized")


# # 메모 삭제
# @app.route('/memos/delete/<int:id>', methods=['DELETE'])
# @login_required
# def delete_memo(id):
#     # memo = Memo.query.filter_by(id=id).first()
#     memo = Memo.query.filter_by(id=id, user_id=current_user.id).first()

#     if memo:
#         db.session.delete(memo)
#         db.session.commit()
#         return jsonify({'message': 'Memo deleted'}), 200
    
#     else:
#         abort(404, description="Memo not found or authorized")


# Flask_Login이 현재 로그인한 사용자를 로드할 수 있도록
# 사용자 로딩 함수를 정의
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))



# # 회원가입 기능
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']

#         existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
#         if existing_user:
#             return jsonify({'error': '사용자 이름 또는 이메일이 이미 사용 중입니다.'}), 400


#         user = User(username=username, email=email)
#         user.set_password(password)

#         db.session.add(user)
#         db.session.commit()

#         return jsonify({'message': '회원가입에 성공했습니다. 기입한 아이디와 패스워드로 로그인할 수 있습니다.'}), 201
    
#     #return render_template('signup.html')
#     return redirect(url_for('home'))


# # 로그인 처리 라우트
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = User.query.filter_by(username = request.form['username']).first()

#         if user and user.check_password(request.form['password']):
#             login_user(user)
#             return jsonify({'message': '로그인에 성공하였습니다. 메모 페이지로 이동합니다.'}), 200
        
#         return jsonify({'error': '아이디가 없거나 패스워드가 다릅니다.'}), 401

#     #return render_template('login.html')
#     return redirect(url_for('home'))


# # 로그아웃 처리 라우트
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     # return jsonify({'message': 'Logged out successfully'}), 200
#     return redirect(url_for('home'))


