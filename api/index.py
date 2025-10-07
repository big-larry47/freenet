# api/index.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="../templates")

# Flask-Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        message_body = request.form.get('message')
        if email and message_body:
            try:
                msg = Message(
                    subject="New Message from Your Form",
                    recipients=[os.getenv("MAIL_USERNAME")]
                )
                msg.body = f"From: {email}\n\nMessage:\n{message_body}"
                mail.send(msg)
            except Exception:
                pass
        return redirect(url_for('index'))
    return render_template('index.html')

# Vercel serverless handler
def handler(request, context):
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app
