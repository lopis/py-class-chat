# sample-web-app/app.py
from flask import Flask, request
import csv
  
app = Flask(__name__)
fieldnames = ['author', 'text']

def loadMessagesFromFile():
    messages = []
    with open('messages.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            messages.append(row)
    return messages

def writeToFile():
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

@app.route('/file') 
def print_file():
    with open('messages.csv') as csv_file:
        text = csv_file.read()
        return text


@app.route('/', methods=['POST'])
def send_message():
    # try:
        message_body = request.form['message']
        message_author = request.form['author']
        messages = loadMessagesFromFile()
        messages.append({
            'author': message_author,
            'text': message_body
        })
        writeToFile()
        return f'Message received! Count: {len(messages) + 1}'
    # except:
    #     return 'Message failed...'