import json
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DATA_FILE = 'posts.json'
ADMIN_PASSWORD = "your_admin_password"  # 管理者パスワード

# データを読み込む関数
def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# データを保存する関数
def save_posts(posts):
    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = load_posts()
    
    # 規約同意チェック（簡易的にCookieやフラグを使うことも可能ですが、今回は初回アクセス時に規約を表示する仕様にできます）
    
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_post = {'id': len(posts), 'content': content}
            posts.append(new_post)
            save_posts(posts)
    
    return render_template('index.html', posts=posts)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    password = request.form.get('password')
    posts = load_posts()
    
    # パスワードチェック（管理者は特定のPW、または投稿者本人のPWなどで分岐可能）
    if password == ADMIN_PASSWORD:
        posts = [p for p in posts if p['id'] != post_id]
        save_posts(posts)
        
    return redirect('/')

if __name__ == '__main__':
    app.run()