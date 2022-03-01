from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
#ahoj

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300))

    def __repr__(self):
        return f'{self.title} - {self.body}'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/posts')
def get_posts():
    posts = Post.query.all()

    output = []
    for post in posts:
        post_data = {'id': post.id, 'user_id': post.user_id, 'title': post.title, 'body': post.body}

        output.append(post_data)

    return {"posts": output}


@app.route('/posts/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return {'id': post.id, 'user_id': post.user_id, 'title': post.title, 'body': post.body}


@app.route('/posts', methods=['POST'])
def add_post():
    response = requests.get('https://jsonplaceholder.typicode.com/users').json()
    userids = [_['id'] for _ in response]

    post = Post(user_id=request.json['user_id'], title=request.json['title'], body=request.json['body'])

    if post.user_id in userids:
        db.session.add(post)
        db.session.commit()
        return {'massage': "post was added"}
    else:
        return {'massage': "wrong userID"}


@app.route('/posts/<id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"error": "not found"}
    else:
        post_to_update = Post(id =request.json['id'], title=request.json['title'], body=request.json['body'])
        db.session.put(post_to_update)
        db.session.commit()
        return {'massage': "post was added"}


@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"error": "not found"}
    db.session.delete(post)
    db.session.commit()
    return {'massage': "post was deleted"}
