from kapsch import os, db

class Photo(db.Model):

    __tablename__ = "photos"
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    img_data = db.Column(db.LargeBinary,nullable=False)
    category = db.Column(db.VARCHAR(1),nullable=True)

    def __init__(self, img_data):
        self.img_data = img_data

def get_image(the_id):
    return Photo.query.filter(Photo.id == the_id).first()



