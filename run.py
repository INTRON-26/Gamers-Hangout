from app import app, db

if(__name__ == "__main__"):
    with app.app_context():
        # Create all the database tables before running the app
        db.create_all()
    app.run()
    