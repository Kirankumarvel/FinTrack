import os
from app import app, db

# Create all required directories
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/charts', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('utils', exist_ok=True)

# Initialize the database
with app.app_context():
    db.create_all()
    print("Database created successfully!")
    print("All directories created successfully!")