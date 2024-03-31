from flask import Flask, render_template, request, redirect, url_for
import string
import secrets
import pyperclip

app = Flask(__name__)

def generate_password(length=12, uppercase=True, lowercase=True, digits=True, symbols=True):
    """Generate a random password."""
    charset = ""
    if uppercase:
        charset += string.ascii_uppercase
    if lowercase:
        charset += string.ascii_lowercase
    if digits:
        charset += string.digits
    if symbols:
        charset += string.punctuation
    
    if not charset:
        raise ValueError("At least one character set must be selected")
    
    password = ''.join(secrets.choice(charset) for _ in range(length))
    return password

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num_passwords = int(request.form['num_passwords'])
            length = int(request.form['length'])
            uppercase = request.form.get('uppercase') == 'on'
            lowercase = request.form.get('lowercase') == 'on'
            digits = request.form.get('digits') == 'on'
            symbols = request.form.get('symbols') == 'on'
        except ValueError:
            error_message = "Invalid input. Please enter valid numbers."
            return render_template('index.html', error_message=error_message)

        passwords = [generate_password(length, uppercase, lowercase, digits, symbols) for _ in range(num_passwords)]
        return render_template('index.html', passwords=passwords)
    return render_template('index.html')

@app.route('/copy', methods=['POST'])
def copy_password():
    password = request.form['password']
    pyperclip.copy(password)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
