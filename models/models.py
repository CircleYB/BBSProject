from datetime import datetime
from database import db


class Post(db.Model):
    __tablename__ = "t_post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    poster_id = db.Column(db.Text())
    poster_name = db.Column(db.Text())
    post_contents = db.Column(db.Text())
    parent_post_id = db.Column(db.Integer)
    ke_id = db.Column(db.Integer, db.ForeignKey('m_thread.id'))
    password = db.Column(db.Text())
    is_delete = db.Column(db.Integer)

    def __init__(self, post_time, poster_id, poster_name, post_contents, parent_post_id, ke_id, password, is_delete):
        self.post_time = post_time
        self.poster_id = poster_id
        self.poster_name = poster_name
        self.post_contents = post_contents
        self.parent_post_id = parent_post_id
        self.ke_id = ke_id
        self.password = password
        self.is_delete = is_delete


class KaThread(db.Model):
    __tablename__ = "m_thread"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class GoodNumber(db.Model):
    __tablename__ = "t_good_number"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('t_post.id'), nullable=False)
    remote_host = db.Column(db.Text(), nullable=False)

    def __init__(self, poster_id, remote_host):
        self.poster_id = poster_id
        self.remote_host = remote_host
