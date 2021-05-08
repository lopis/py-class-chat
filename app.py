# sample-web-app/app.py
from flask import Flask, request
import csv
  
app = Flask(__name__)
messages = []
fieldnames = ['author', 'text']

with open('messages.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for index in range(csv_reader):
        if index > 1:
            messages.append(csv_reader(index))

def writeToFile():
    with open('messages.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for message in messages:
            writer.writerow(message)

def getMessagesAsString():
    all_messages = f'<h2>Messages ({len(messages)}):</h2>'
    for message in messages:
        all_messages += f'<p><strong>[{message.name}]:</strong> {message.text}</p>'
    return all_messages
  
@app.route('/') 
def home_view(): 
    messages_as_string = getMessagesAsString()
    return f"<h1>Welcome to the class chat!</h1>{messages_as_string}"

@app.route('/file') 
def print_file():
    with open('messages.csv') as csv_file:
        text = csv_file.read()
        return text


@app.route('/', methods=['POST'])
def send_message():
    try:
        message_body = request.form['message']
        message_author = request.form['author']
        messages.append({
            'author': message_author,
            'text': message_body
        })
        writeToFile()
        return f'Message received! Count: {len(messages)}'
    except:
        return 'Message failed...'