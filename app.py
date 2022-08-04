# importing the flask dependency

from flask import Flask

# Creating a New Flask App Instance
# instance is a general term in programming referring to a singular version of something.

app = Flask(__name__)
# here, the __name__ is a magic method that denotes the name of the current function. 
# can use the __name__ function if code is run from command line or important from another piece of code.

# Creating the Flask Routes
# First define the starting point called the route
# use the following function:
# The / indicates that we want to put our data at the root of our routes
# The / is commonly known as the highest level of hierarchy in any computer system.

@app.route('/')

def hello_world():
    return 'Hello World'

@app.route('/Homepage')

def home_page():
    return 'This is the homepage. Welcome home.'

# to run the app, use environment variable by putting export FLASK_APP=app.py
# do this after navigating the directory where app.py is saved.