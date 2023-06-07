from flask import Flask,render_template,flash, redirect,url_for,session,logging,request,send_file
from flask_sqlalchemy import SQLAlchemy
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/LENOVO/PycharmProjects/flaskProject/file.db'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    sname = db.Column(db.String(80))
    address = db.Column(db.String(120))
    postcode = db.Column(db.String(20))
    city = db.Column(db.String(80))
    country = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    height = db.Column(db.String(10))

def func(input_file, output_file, user_data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(128, 460, user_data.name)
    can.drawString(128, 438, user_data.sname)
    can.drawString(128, 417, user_data.address)
    can.drawString(128, 396, user_data.postcode)
    can.drawString(128, 375, user_data.city)
    can.drawString(128, 353, user_data.country)
    can.drawString(128, 332, user_data.gender)
    can.drawString(128, 311, user_data.height)
    can.save()

    packet.seek(0)

    new_pdf = PdfFileReader(packet)

    existing_pdf = PdfFileReader(open(input_file, "rb"))
    output = PdfFileWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    output_stream = open(output_file, "wb")
    output.write(output_stream)
    output_stream.close()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        login = user.query.filter_by(username=uname, password=passw).first()

        if login is not None:
            return redirect(url_for("dashboard", uname=uname, passw=passw))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard/<uname>/<passw>", methods=["GET", "POST"])
def dashboard(uname, passw):
    if request.method == "POST":
        # Retrieve the form data
        name = request.form.get('name')
        sname = request.form.get('sname')
        address = request.form.get('address')
        postcode = request.form.get('postcode')
        city = request.form.get('city')
        country = request.form.get('country')
        gender = request.form.get('gender')
        height = request.form.get('height')

        # Update the user record in the database
        user_data = user.query.filter_by(username=uname, password=passw).first()
        user_data.name = name
        user_data.sname = sname
        user_data.address = address
        user_data.postcode = postcode
        user_data.city = city
        user_data.country = country
        user_data.gender = gender
        user_data.height = height
        db.session.commit()

        return redirect(url_for("updated_details", uname=uname, passw=passw))
    return render_template("dashboard.html", uname=uname, passw=passw)

@app.route("/updated_details/<uname>/<passw>")
def updated_details(uname, passw):
    user_data = user.query.filter_by(username=uname, password=passw).first()
    return render_template("updated_details.html", user=user_data)

@app.route("/motor_insurance/<username>/<password>")
def motor_insurance(username, password):
    user_data = user.query.filter_by(username=username, password=password).first()
    if user_data:
        input_file = "static/Motor.pdf"
        output_file = "static/MI.pdf"
        func(input_file, output_file, user_data)
        return send_file(output_file, mimetype='MI/pdf')
    else:
        return "User not found"

@app.route("/life_insurance/<username>/<password>")
def life_insurance(username, password):
    user_data = user.query.filter_by(username=username, password=password).first()
    if user_data:
        input_file = "static/Life.pdf"
        output_file = "static/LI.pdf"
        func(input_file, output_file, user_data)
        return send_file(output_file, mimetype='LI/pdf')
    else:
        return "User not found"

@app.route("/health_insurance/<username>/<password>")
def health_insurance(username, password):
    user_data = user.query.filter_by(username=username, password=password).first()
    if user_data:
        input_file = "static/Health.pdf"
        output_file = "static/HEI.pdf"
        func(input_file, output_file, user_data)
        return send_file(output_file, mimetype='HEI/pdf')
    else:
        return "User not found"

@app.route("/home_insurance/<username>/<password>")
def home_insurance(username, password):
    user_data = user.query.filter_by(username=username, password=password).first()
    if user_data:
        input_file = "static/Home.pdf"
        output_file = "static/HI.pdf"
        func(input_file, output_file, user_data)
        return send_file(output_file, mimetype='hI/pdf')
    else:
        return "User not found"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)