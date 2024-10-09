from app import create_app
from models import db, user_datastore

app, _ = create_app()

def create_empty_tables():
    db.drop_all()
    db.create_all()