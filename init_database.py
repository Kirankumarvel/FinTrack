import os
from app import app, db

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

def init_db():
    # Create charts directory if it doesn't exist
    charts_path = os.path.join(basedir, 'static', 'charts')
    if not os.path.exists(charts_path):
        os.makedirs(charts_path)
    
    with app.app_context():
        db.create_all()
        print("Database created successfully!")

if __name__ == '__main__':
    init_db()