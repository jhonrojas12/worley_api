from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess

app = Flask(__name__)

# Configuración del servidor de correo
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'jrojas.correo123@gmail.com'  # Tu dirección de correo electrónico
SMTP_PASSWORD = 'pngb ylnh bclw xljg'  # Contraseña de aplicación específica

# Ruta para mostrar el formulario
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Ruta para procesar la palabra y el correo electrónico
@app.route('/submit', methods=['POST'])
def submit():
    word = request.form.get('word')
    email = request.form.get('email')

    if word and email:
        # Guardar la palabra en un archivo de texto
        with open('words.txt', 'a') as file:
            file.write(word + '\n')

        # Ejecutar el script database.py y pasar la palabra como parámetro
        run_database_script(word)

        # Enviar un saludo al correo electrónico
        #send_email(email, word)

    return redirect(url_for('index'))

def run_database_script(word):
    try:
        # Ejecutar el script database.py con la palabra como argumento
        result = subprocess.run(['python', 'database.py', word], capture_output=True, text=True)
        print(f"Script output: {result.stdout}")
        if result.stderr:
            print(f"Script error: {result.stderr}")
    except Exception as e:
        print(f"Failed to run script: {e}")

def send_email(to_email, word):
    from_email = SMTP_USERNAME
    subject = 'Thank You for Your Submission'
    body = f'Hello,\n\nThank you for submitting the word "{word}". We appreciate your contribution!\n\nBest regards,\nYour Team'

    # Configurar el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Enviar el mensaje
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Identificarse con el servidor
            server.starttls()  # Iniciar TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
