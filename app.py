#!flask/bin/python
from datetime import timedelta
from flask import Flask, jsonify, abort, make_response, request, url_for, current_app
from flask.ext.httpauth import HTTPBasicAuth
from functools import update_wrapper

''' Decorator to allow crossdomain access '''
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



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

@app.route('/chat/api/v1.0/chats', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_chats():
    return jsonify({'chats': [make_public_chat(chat) for chat in chats]})

@app.route('/chat/api/v1.0/chats/<int:chat_id>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_chat(chat_id):
    chat = [chat for chat in chats if chat['id'] == chat_id]
    if len(chat) == 0:
        abort(404)
    return jsonify({'chat': chat[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/chat/api/v1.0/chats', methods=['POST'])
@crossdomain(origin='*')
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
