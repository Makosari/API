from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(50))
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


@app.route('/posts/<search>/<id>', methods=['GET'])
def get_post_or_posts(search, id):
    data = []
    if search == 'user':
        post = Post.query.get()
        return {"daco": data}

    elif search == 'post':
        post = Post.query.get(id)
        if post is None:
            response = requests.get('https://jsonplaceholder.typicode.com/posts').json()
            postid = [_['id'] for _ in response]
            if int(id) in postid:
                return {'massage': "Post was found and added."}
            else:
                return {'massage': "Post does not exist here."}
        else:
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
        updated = Post(title=request.json['title'], body=request.json['body'])
        db.session.add(updated)
        db.session.commit()
        return {'massage': "post was updated"}


@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"error": "not found"}
    db.session.delete(post)
    db.session.commit()
    return {'massage': "post was deleted"}


if __name__ == "__main__":
    app.run()
