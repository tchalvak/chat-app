#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

''' Simple Flask REST API
    Sample urls:
    http://127.0.0.1:5000/chat/api/v1.0/chats
'''




chats = [
    {
        'id': 1,
        'username': u'Roy',
        'chat': u'This is totally a chat yeah, really.',
        'done': False
    },
    {
        'id': 2,
        'username':u'Bob',
        'chat': u'Yes, I am glad you created this chat.  Definitely.',
        'done': False
    }
]


@auth.get_password
def get_password(username):
    # Totally fake auth stuff for now
    if username == 'sesame':
        return 'open'
    return None

@auth.error_handler
def unauthorized():
    #Return 403 to prevent browsers from url prompting on unauth.
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/chat/api/v1.0/chats', methods=['GET'])
def get_chats():
    return jsonify({'chats': [make_public_chat(chat) for chat in chats]})

@app.route('/chat/api/v1.0/chats/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = [chat for chat in chats if chat['id'] == chat_id]
    if len(chat) == 0:
        abort(404)
    return jsonify({'chat': chat[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/chat/api/v1.0/chats', methods=['POST'])
@auth.login_required
def create_chat():
    if not request.json or not 'title' in request.json:
        abort(400)
    chat = {
        'id': chats[-1]['id'] + 1,
        'username':request.json['username'],
        'chat':request.json.get('chat', ''),
        'done': False
    }
    chats.append(chat)
    return jsonify({'chat': chat}), 201

@app.route('/chat/api/v1.0/chats/<int:chat_id>', methods=['PUT'])
@auth.login_required
def update_chat(chat_id):
    chat = [chat for chat in chats if chat['id'] == chat_id]
    if len(chat) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    chat[0]['title'] = request.json.get('title', chat[0]['title'])
    chat[0]['description'] = request.json.get('description', chat[0]['description'])
    chat[0]['done'] = request.json.get('done', chat[0]['done'])
    return jsonify({'chat': chat[0]})

@app.route('/chat/api/v1.0/chats/<int:chat_id>', methods=['DELETE'])
@auth.login_required
def delete_chat(chat_id):
    chat = [chat for chat in chats if chat['id'] == chat_id]
    if len(chat) == 0:
        abort(404)
    chats.remove(chat[0])
    return jsonify({'result': True})

def make_public_chat(chat):
    new_chat = {}
    for field in chat:
        if field == 'id':
            new_chat['uri'] = url_for('get_chat', chat_id=chat['id'], _external=True)
        else:
            new_chat[field] = chat[field]
    return new_chat

if __name__ == '__main__':
    app.run(debug=True)
