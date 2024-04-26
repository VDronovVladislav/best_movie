import os

from . import db, app


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(255))

    def get_image_path(self):
        if self.image.startswith('https'):
            return self.image
        return os.path.join(app.config['UPLOAD_FOLDER'], self.image)
