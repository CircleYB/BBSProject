from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length


class WriteForm(FlaskForm):
    poster_name = StringField('投稿者', validators=[DataRequired(), Length(max=10, message="名前は10文字以下で")])
    post_contents = TextAreaField('内容(必須)', validators=[DataRequired()])
    delete_password = PasswordField('削除キー', validators=[Length(min=0, max=6, message="削除キーは6文字以下で")])
    submit = SubmitField('確認する')
