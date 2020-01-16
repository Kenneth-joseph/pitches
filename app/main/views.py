from flask import render_template,redirect,url_for,request,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Comment,Pitch,Upvote,Downvote
from .form import Updateprofile,Topicform,CommentForm
from .. import db

@main.route('/')
def index():
   
    return render_template('index.html')

@main.route('/create_new',methods=['GET','POST'])
@login_required
def new_pitch():
    form=Topicform()
    if form.validate_on_submit():
        title=form.title.data
        post=form.post.data
        category=form.category.data
        user_id=current_user
        new_pitch_object=Pitch(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_pitchez()
        return redirect(url_for('main.index'))
    return render_template('pitch.html',form=form)


@main.route('/comment/<int:pitch_id>',methods=['GET','POST'])
@login_required
def comment(pitch_id):
    form=CommentForm()
    pitch=Pitch.query.get(pitch_id)
    all_comment=Comment.query.filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        comment= form.comment.data
        pitch_id= pitch_id
        user_id=current_user._get_current_object().id
        new_comment = Comment(comment=comment,pitch_id=pitch_id,user_id=user_id)
        new_comment.save_comment()
        return redirect(url_for('.comment',pitch_id=pitch_id))
    return render_template('comment.html',pitch=pitch,form=form,all_comment=all_comment)


@main.route('/user/<name>')
def profile(name):
    user=User.query.filter_by(username=name).first()
    user_id = current_user._get_current_object().id
    posts=Pitch.query.filter_by(user_id=user_id).all()
    if user is None:
        abort(404)
    return render_template("profile/profile.html",user= user,posts=posts)


@main.route('/user/<name>/updateprofile',methods=['GET','POST'])
@login_required
def updateprofile(name):
    form = Updateprofile()
    user= User.query.filter_by(username = name).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for('.profile',name=name))
    return render_template('profile/update.html' ,form=form)


@main.route('/like/<int:id>',methods=['GET','POST'])
@login_required
def like(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pit in get_pitches:
        to_str = f'{pit}'
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user=current_user,pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))


main.route('/dislike/<int:id>',methods=['GET','POST'])
@login_required
def dislike(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user=current_user,pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id=id))


