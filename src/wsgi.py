# This file was created to run the application on heroku using gunicorn.
# Read more about it here: 
from app import app as application

if __name__ == "__main__":
    application.run()
