from base64 import b64encode
from base64 import b64decode
from binascii import Error
from flask import escape
from flask import Flask
from flask import request

app = Flask(__name__)


defaultText = 'Hello less and less Cloudy World v2!'


def __encrypt(plainText):
    # args: a single utf-8 encoded string
    # return: an utf-8 encoded string
    return b64encode(plainText.encode('utf-8')).decode('utf-8')


def __decrypt(encryptedText):
    # args: a single utf-8 encoded string
    # return: a tuple with return status and the result as utf-8 encoded string
    try:
        return ('success', b64decode(encryptedText.encode('utf-8')).decode('utf-8'))
    except UnicodeDecodeError:
        return ('failed', 'Error while decoding the input string')
    except Error:
        return ('failed', 'Error while decoding the input string')


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
        encryptedText = __encrypt(plainText)
        output = '<p>Here is your encrypted text:</p>\n'
        output += '<pre>\n'
        output += f'{encryptedText}\n'
        output += '</pre>\n'
    else:
        output = '<p>You do not provided the text to encrypt.<br>\n'
        output += f'Please give me your plain text using <code>{escape("?text=<your_text_here>")}</code></p>'
    return output


@app.route('/decrypt')
def decrypt():
    encryptedText = request.args.get('text')
    if encryptedText:
        decryptStatus, decryptedText = __decrypt(encryptedText)
        if decryptStatus == 'success':
            output = '<p>Here is your decrypted text:</p>\n'
            output += '<pre>\n'
            output += f'{escape(decryptedText)}\n'
            output += '</pre>\n'
        else:
            output = f'<p><span style="color: red;">Error: {escape(decryptedText)}</span></p>'
    else:
        output = '<p>You do not provided the text to decrypt.<br>\n'
        output += f'Please give me your encrypted text using <code>{escape("?text=<your_text_here>")}</code></p>'
    return output


app.run(host='0.0.0.0')
