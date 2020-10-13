from flask import Flask, render_template

app = Flask(__name__)

myposts = [{'id':1,'title':'first post', 'content':'post 1', 'created':'today'},
        {'id':2,'title':'second post','content':'post 2', 'created':'yesterday'}]

@app.route('/')
def index():
    return render_template('index.html', posts=myposts) 

def get_post(post_id):
    post = myposts[post_id-1]
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
