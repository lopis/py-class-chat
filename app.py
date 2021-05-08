# sample-web-app/app.py
from flask import Flask, request
  
app = Flask(__name__)
messages = []

def getMessagesAsString():
    all_messages = ''
    for message in messages:
        all_messages += f'<p><strong>[{message.name}]:</strong> {message.text}</p>'
    return all_messages
  
@app.route('/') 
def home_view(): 
    messages_as_string = getMessagesAsString()
    return f"<h1>Welcome to the class chat!</h1>{messages_as_string}"

@app.route('/', methods=['POST'])
def send_message():
    try:
        message_body = request.form['message']
        message_author = request.form['author']
        messages.append({
            'author': message_author,
            'text': message_body
        })
        return 'Message received!'
    except:
        return 'Message failed...'