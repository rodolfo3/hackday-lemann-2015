from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return ":)"

import school
school.include_me(app)

import students
students.include_me(app)

if __name__ == '__main__':
    app.run(debug=True)
