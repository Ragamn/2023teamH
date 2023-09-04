from flask import Flask, render_template,request,redirect,url_for,session
import db,string,random,os
from datetime import timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

if __name__ == '__main__':
    app.run(debug=True)
    






#投稿削除機能
##データベースモデルに変更

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deleted = db.Column(db.Boolean, default=False)  # 削除フラグ

##投稿の削除ビューの更新
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # 投稿のユーザーIDがログインユーザーのIDと一致する場合にのみ削除を許可
    if post.user_id == current_user.id:
        post.deleted = True  # 削除フラグを立てる
        db.session.commit()
    
    return redirect(url_for('view_posts'))

