from flask import Flask, request, render_template, make_response, session, redirect, url_for, Markup
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from datetime import datetime
from database import init_db
from database import db
import models
import uuid
import random
import re
from string import ascii_letters, digits
from form import WriteForm


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    init_db(app)
    return app


app = create_app()

admin = Admin(app)
admin.add_view(ModelView(models.Post, db.session))


def generate_form_token():
    """Sets a token to prevent double posts."""
    if '_form_token' not in session:
        form_token = ''.join([random.choice(ascii_letters + digits) for i in range(32)])
        session['_form_token'] = form_token
    return session['_form_token']


# jinja2によるCustom filter method
@app.template_filter('add_anchor')
def add_anchor(s, ke_id):
    m = re.match(r'>>\d+', s)
    idx_start = m.start()
    idx_end = m.end()
    article_number = m.group().strip(">>")

    aa = ('<a href="%s">%s</a>' % ("/ke?ke_id=" + str(ke_id) + "&article_number=" + article_number, m.group()))
    result = s[:idx_start] + aa + s[idx_end:]

    return result


@app.template_filter('cr')
def cr(arg):
    return Markup(arg.replace('\n', '<br>'))


@app.route("/")
def index():
    # トップ画面。データベースから全ての卦を読み込む
    ke_order = db.session.query(models.Post.ke_id, func.max(models.Post.post_time).label("max_time")).group_by(models.Post.ke_id).subquery()
    threads = db.session.query(models.KaThread.id, models.KaThread.name).outerjoin(ke_order, models.KaThread.id == ke_order.c.ke_id).order_by(ke_order.c.max_time.desc()).all()
    # threads = db.session.query(models.KaThread.name).all()
    response = make_response(render_template("index.html", threads=threads))

    # 以下、Cookieの設定。始めにCookieの有効期限の設定を取得
    max_age = 60 * 60 * 24 * 365 * 2  # 2 years
    expires = int(datetime.now().timestamp()) + max_age

    if 'eki_bbs_unique_id' in request.cookies:
        user_name = request.cookies.get('eki_bbs_unique_id')
        response.set_cookie('eki_bbs_unique_id', value=user_name, max_age=max_age, expires=expires, path='/', domain='127.0.0.1:5000', secure=False, httponly=True)
    else:
        # cookieが存在しない場合、idとしてuuidを付与する。
        visitor_id = str(uuid.uuid4())
        response.set_cookie('eki_bbs_unique_id', value=visitor_id, max_age=max_age, expires=expires, path='/', domain='127.0.0.1:5000', secure=False, httponly=True)

    return response


@app.route('/ke', methods=['GET'], defaults={'page': 1})
@app.route('/ke/<int:page>', methods=['GET'])
def ke(page):
    per_page = 50

    # データベースから読み込む
    ke_id = request.args.get('ke_id', type=int)
    article_number = request.args.get('article_number', 0, type=int)
    ke_name = db.session.query(models.KaThread.name).filter_by(id=ke_id).all()

    # データベースから各投稿を読み込む。
    if article_number > 0:
        articles = models.Post.query.filter_by(ke_id=ke_id).offset(article_number).limit(1)
    else:
        articles = models.Post.query.filter_by(ke_id=ke_id).order_by(models.Post.id.desc()).paginate(page, per_page, error_out=False)

    return render_template("ke.html", ke_id=ke_id, ke_name=ke_name[0][0], articles=articles)


@app.route("/form", methods=['GET', 'POST'])
def form_check():
    ke_id = request.args.get('ke_id', type=int)
    article_number = request.args.get('article_number', type=int)
    ke_name = db.session.query(models.KaThread.name).filter_by(id=ke_id).all()
    app.jinja_env.globals['form_token'] = generate_form_token()

    form = WriteForm()
    if article_number > 0:
        form.post_contents.data = ">>" + str(article_number)

    if form.validate_on_submit():
        # validationが通ったら、requestでke_id・poster_name・post_contentsの値を取得する
        poster_name = request.form['poster_name']
        post_contents = request.form['post_contents']

        return redirect(url_for('confirm', ke_id=ke_id, poster_name=poster_name, post_contents=post_contents))

    return render_template('form.html', ke_id=ke_id, ke_name=ke_name[0][0], form=form)


@app.route("/confirm", methods=['GET'])
def confirm():
    ke_id = request.args.get('ke_id', type=int)
    poster_name = request.args.get('poster_name')
    post_contents = request.args.get('post_contents')
    print(post_contents)

    return render_template("confirm.html", ke_id=ke_id, poster_name=poster_name, post_contents=post_contents)


@app.route("/post", methods=['POST'])
def post():
    """Checks for a valid form token in POST requests."""
    if request.method == 'POST':
        token = session.pop('_form_token', None)
        if not token or token != request.form['_form_token']:
            return redirect(url_for('index'))

    # ここからDBへ書き込み内容を記入する。
    # requestでarticleとnameの値を取得する
    # post_time = int(datetime.now().timestamp())
    post_time = datetime.now()

    poster_name = request.form['poster_name']
    post_contents = request.form['post_contents']

    print(post_contents)

    # parent_post_id = request.form['parent_id']
    parent_post_id = 0
    ke_id = request.form['ke_id']
    # password = request.form['password']
    password = "aaa"

    # 以下、cookieから取得
    poster_id = request.cookies.get('eki_bbs_unique_id')

    admin = models.Post(post_time=post_time, poster_id=poster_id, poster_name=poster_name, post_contents=post_contents,
                        parent_post_id=parent_post_id, ke_id=ke_id, password=password, is_delete=0)
    db.session.add(admin)
    db.session.commit()

    # session['ke_id'] = ke_id
    return redirect(url_for('complete', ke_id=ke_id))


@app.route("/complete")
def complete():
    # if 'ke_id' not in session:
    #     return redirect(url_for('index'))
    ke_id = request.args.get('ke_id', type=int)
    return render_template("complete.html", ke_id=ke_id)


if __name__ == "__main__":
    app.run(debug=True)
