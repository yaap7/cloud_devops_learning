from base64 import b64encode
from base64 import b64decode
from flask import escape
from flask import Flask
from flask import request

app = Flask(__name__)


defaultText = 'Hello Cloudy World!'


def _encrypt(plainText):
    # args: a single utf-8 encoded string
    # return: an utf-8 encoded string
    return b64encode(plainText.encode('utf-8')).decode('utf-8')


def _decrypt(encryptedText):
    # args: a single utf-8 encoded string
    # return: an utf-8 encoded string
    return b64decode(encryptedText.encode('utf-8')).decode('utf-8')


@app.route('/')
def hello_cloud():
    name = request.args.get('name')
    if name:
        return f'Hello {escape(name)}'
    else:
        return defaultText


@app.route('/encrypt')
def encrypt():
    plainText = request.args.get('text')
    if plainText:
        encryptedText = _encrypt(plainText)
        output = '<p>Here is your encrypted text:</p>\n'
        output += '<pre>\n'
        output += f'{encryptedText}\n'
        output += '</pre>\n'
    else:
        output = '<p>You do not provided the text to encrypt.<br>\n'
        output += f'Please give me your plain text using <code>{escape("?text=<your_text_here>")}</code></p>'
    return output


app.run(host='0.0.0.0')
