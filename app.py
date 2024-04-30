from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///applications.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "eseosehodion@gmail.com"
app.config["MAIL_PASSWORD"] = "folu ndoo umil zuto"

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(89))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route("/", methods=["GET", "POST"]) # the homepage is represented by "/" always
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"""
        Thank you for your submission, {first_name}.
        Here are your data:
        Name: {first_name} {last_name}
        Date: {date_obj}
        Occupation: {occupation}
        Thank you.
        """
        message = Message(subject="New form submission",
                       sender=app.config['MAIL_USERNAME'],
                       recipients=[email],
                       body=message_body)
        mail.send(message)

     
        flash(f"{first_name}, your form was submitted successfully!", "success")

        
    return render_template("index.html")
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5002)