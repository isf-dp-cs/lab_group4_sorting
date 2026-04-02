from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    science1 = db.Column(db.String(120), unique=False, nullable=False)
    science2 = db.Column(db.String(120), unique=False, nullable=False)
    science3 = db.Column(db.String(120), unique=False, nullable=False)

    group_num = db.Column(db.Integer, unique=False, nullable=False, default=0)


    def __repr__(self):
        return f"{self.name} ({self.science1}, {self.science2}, {self.science3}) (Group {self.group_num})" 
    
