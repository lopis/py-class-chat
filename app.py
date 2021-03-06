# sample-web-app/app.py
from flask import Flask, request
import csv
import json 

app = Flask(__name__)
fieldnames = ['author', 'text']

def loadMessagesFromFile():
    messages = []
    with open('messages.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            messages.append(row)
    return messages

def writeToFile(messages):
    with open('messages.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for message in messages:
            writer.writerow(message)

def getMessagesAsString():
    messages = loadMessagesFromFile()
    all_messages = f'<h2>Messages ({len(messages)}):</h2>'
    for message in messages:
        try:
            all_messages += f'<p><strong>[{message["author"]}]:</strong> {message["text"]}</p>'
        except:
            all_messages += f'~{message}'
    return all_messages
  
@app.route('/') 
def home_view(): 
    messages_as_string = getMessagesAsString()
    return f"<h1>Welcome to the class chat!</h1>{messages_as_string}"
      
@app.route('/get_messages') 
def json_view(): 
    messages = loadMessagesFromFile()
    messages_as_json = json.dumps(messages)
    return messages_as_json

@app.route('/file') 
def print_file():
    with open('messages.csv') as csv_file:
        text = csv_file.read()
        return text


@app.route('/', methods=['POST'])
def send_message():
    # try:
        message_body = request.form['message']
        if len(message_body) > 140:
            return 'Your message is too long'
        elif len(message_body) < 1:
            return 'Your message is too small'

        message_author = request.form['author']
        if len(message_author) > 10:
            return 'Your name is too long'
        elif len(message_author) < 5:
            return 'Your name is too short (min 5)'

        messages = loadMessagesFromFile()
        messages.append({
            'author': message_author,
            'text': message_body
        })
        writeToFile(messages)
        return f'Message received! Count: {len(messages)}'
    # except:
    #     return 'Message failed...'