from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isnumeric():
            raise ValueError("phone must be 10 digits")
        return phone_number
    
    
    @validates('name')
    def validate_name(self, key, name):
        exists = Author.query.filter(Author.name == name).first()
        if name == "":
            raise ValueError("name cant be empty string")
        if exists:
            raise ValueError("name already exists")
        return name
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        clickbaits = ["Won't Believe", "Secret", "Top", "Guess"]
        exists = Post.query.filter(Post.title == title).first()
        if title == "":
            raise ValueError("title cant be empty string")
        if exists:
            raise ValueError("title already exists")
        for cb in clickbaits:
            if cb in title:
                return title
        raise ValueError("title not click baity enough")
        
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content too short. Less than 250 chars.")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Content too long. More than 250 chars.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("category must be fiction or non-fiction")
        return category
    
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
