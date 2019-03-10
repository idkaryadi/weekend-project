from blueprints import db
from flask_restful import fields

class Users(db.Model):

    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.String(10))
    # created_at = db.Column(db.DataTime)
    # updated_at = db.Column(db.DataTime)
    # deleted_at = db.Column(db.DataTime)

    respond_field = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.String
        # 'created_at' : fields.DataTime,
        # 'updated_at' : fields.DataTime,
        # 'deleted_at' : fields.DataTime
    }

    def __init__(self, id, username, password, status): # created_at, updated_at, deleted_at
        self.id = id
        self.username = username
        self.password = password
        self.status = status
        # self.created_at = created_at
        # self.updated_at = updated_at
        # self.deleted_at = deleted_at

    def __repr__(self):
        return '<Users %r>' % self.id

class Clients(db.Model):

    __tablename__ = "Clients"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.String(10))
    # created_at = db.Column(db.DataTime)
    # updated_at = db.Column(db.DataTime)
    # deleted_at = db.Column(db.DataTime)

    respond_field = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.String
        # 'created_at' : fields.DataTime,
        # 'updated_at' : fields.DataTime,
        # 'deleted_at' : fields.DataTime
    }

    def __init__(self, id, username, password, status): # created_at, updated_at, deleted_at
        self.id = id
        self.username = username
        self.password = password
        self.status = status
        # self.created_at = created_at
        # self.updated_at = updated_at
        # self.deleted_at = deleted_at

    def __repr__(self):
        return '<Clients %r>' % self.id

class Admins(db.Model):

    __tablename__ = "Admins"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    status = db.Column(db.String(10))
    # created_at = db.Column(db.DataTime)
    # updated_at = db.Column(db.DataTime)
    # deleted_at = db.Column(db.DataTime)

    respond_field = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.String
        # 'created_at' : fields.DataTime,
        # 'updated_at' : fields.DataTime,
        # 'deleted_at' : fields.DataTime
    }

    def __init__(self, id, username, password, status): # created_at, updated_at, deleted_at
        self.id = id
        self.username = username
        self.password = password
        self.status = status
        # self.created_at = created_at
        # self.updated_at = updated_at
        # self.deleted_at = deleted_at

    def __repr__(self):
        return '<Admins %r>' % self.id
