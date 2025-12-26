from flask import render_template, request, jsonify, abort, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Memo
from login_manager import login_manager

def setup_routes(app):

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 기존 라우트
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return '이것은 마이 메모 앱의 소개 페이지입니다.'
    
    # 로그인 처리 라우트
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(username = request.form['username']).first()

            if user and user.check_password(request.form['password']):
                login_user(user)
                return jsonify({'message': '로그인에 성공하였습니다. 메모 페이지로 이동합니다.'}), 200
            
            return jsonify({'error': '아이디가 없거나 패스워드가 다릅니다.'}), 401

        #return render_template('login.html')
        return redirect(url_for('home'))


    # 로그아웃 처리 라우트
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        # return jsonify({'message': 'Logged out successfully'}), 200
        return redirect(url_for('home'))


    # 회원가입 기능
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                return jsonify({'error': '사용자 이름 또는 이메일이 이미 사용 중입니다.'}), 400


            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return jsonify({'message': '회원가입에 성공했습니다. 기입한 아이디와 패스워드로 로그인할 수 있습니다.'}), 201
        
        #return render_template('signup.html')
        return redirect(url_for('home'))
    

    # 메모 생성
    @app.route('/memos/create', methods=['POST'])
    @login_required
    def create_memo():
        title = request.json['title']
        content = request.json['content']
        # new_memo = Memo(title=title, content=content)
        new_memo = Memo(user_id=current_user.id, title=title, content=content)
            # 헤당 메모가 어떤 사용자에 의해 작성된건지 식별 가능
        db.session.add(new_memo)
        db.session.commit()

        return jsonify({'message': 'Memo created'}), 201
    

    # 메모 조회
    @app.route('/memos', methods=['GET'])
    @login_required
    def list_memos():
        # memos = Memo.query.all()
        #return jsonify([{'id': memo.id, 'title': memo.title, 'content': memo.content} for memo in memos]), 200
        memos = Memo.query.filter_by(user_id=current_user.id).all()
        return render_template('memos.html', memos=memos, username=current_user.username)
    

    # 메모 업데이트
    @app.route('/memos/update/<int:id>', methods=['PUT'])
    @login_required
    def update_memo(id):
        # memo = Memo.query.filter_by(id=id).first()
        memo = Memo.query.filter_by(id=id, user_id=current_user.id).first() # 현재 사용자의 메모만 선택

        if memo:
            memo.title = request.json['title']
            memo.content = request.json['content']
            db.session.commit()
            return jsonify({'message': 'Memo updated'}), 200
        
        else:
            abort(404, description="Memo not found or authorized")


    # 메모 삭제
    @app.route('/memos/delete/<int:id>', methods=['DELETE'])
    @login_required
    def delete_memo(id):
        # memo = Memo.query.filter_by(id=id).first()
        memo = Memo.query.filter_by(id=id, user_id=current_user.id).first()

        if memo:
            db.session.delete(memo)
            db.session.commit()
            return jsonify({'message': 'Memo deleted'}), 200
        
        else:
            abort(404, description="Memo not found or authorized")

