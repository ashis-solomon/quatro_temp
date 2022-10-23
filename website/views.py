from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Post, User
from . import db
from . import ma
import json
from datetime import datetime


views = Blueprint('views', __name__)

# -------------------------------------------------------------------------------------------------------------------
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'email', 'first_name')
    # fields = ('id', 'email', 'password', 'first_name', 'notes', 'org_bool', 'org_name', 'org_volunteers', 'org_lat', 'org_long')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
class OrgSchema(ma.Schema):
  class Meta:
    fields = ('id', 'email', 'org_name', 'org_types', 'org_volunteers', 'org_lat', 'org_long')
    # fields = ('id', 'email', 'password', 'notes', 'org_bool', 'org_name', 'org_types', 'org_volunteers', 'org_lat', 'org_long')

org_schema = OrgSchema()
orgs_schema = OrgSchema(many=True)
# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
class PostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'emailID', 'type', 'lat', 'long', 'active', 'time')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
# -------------------------------------------------------------------------------------------------------------------


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# -------------------------------------------------------------------------------------------------------------------
# view all users
@views.route('/user', methods=['GET'])
# @login_required
def get_users():
    all_users = User.query.filter_by(org_bool=0)
    # all_users = User.query.all()
    # all_products = Post.query.first()
    # result = post_schema.dump(all_products)
    result = users_schema.dump(all_users)
    return jsonify(result)

# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
# view all organizations
@views.route('/orgs', methods=['GET'])
# @login_required
def get_orgs():
    all_orgs = User.query.filter_by(org_bool=1)
    result = orgs_schema.dump(all_orgs)
    return jsonify(result)

# -------------------------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------------------------

# add a post
@views.route('/post', methods=['POST'])
# @login_required
def add_post():
    emailID = request.json['emailID']
    type = request.json['type']
    lat = request.json['lat']
    long = request.json['long']
    active = 1
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y,%H:%M:%S")
    print(dt_string)
    time = dt_string
    if Post.query.filter_by(emailID=emailID).first() is not None:
        return f'POST by user {emailID} already exists !!'
    else:
        # user_id = request.json['user_id']
        # print(request)
        new_post = Post(emailID=emailID, type=type, lat=lat, long=long, active=active, time=time)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added!', category='success')
        return jsonify(post_schema.dump(new_post))
        return "added"


# get all posts
@views.route('/post', methods=['GET'])
# @login_required
def get_posts():
    all_posts = Post.query.all()
    # all_products = Post.query.first()
    # result = post_schema.dump(all_products)
    result = posts_schema.dump(all_posts)

    return jsonify(result)
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

# get a single post by id
@views.route('/post/filter/id=<id>', methods=['GET'])
# @login_required
def get_single_post_id(id):
    post = Post.query.get(id)
    result = post_schema.dump(post)
    return jsonify(result)

# get a single post filter by email
@views.route('/post/filter/email=<email>', methods=['GET'])
# @login_required
def get_single_post_email(email):
    post = Post.query.filter_by(emailID=email).first()
    result = post_schema.dump(post)
    return jsonify(result)

# get a single post filter by email and id
@views.route('/post/filter/email=<email>/id=<id>', methods=['GET'])
# @login_required
def get_single_post_email_(email,id):
    post = Post.query.filter_by(emailID=email).filter_by(id=id).first()
    result = post_schema.dump(post)
    return jsonify(result)

# -------------------------------------------------------------------------------------------------------------------
