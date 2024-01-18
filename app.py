from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        with app.app_context():  # Set up application context
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])

            new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

        return 'Регистрация успешно завершена!'
    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():  # Set up application context
        db.create_all()
    app.run(debug=True)