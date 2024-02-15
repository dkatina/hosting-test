from flask import request, jsonify
from . import api
from app.models import Posts

@api.post('/create_post')
def create_post():
    print('in post')
    data = request.get_json()
    print(data)
    new_post = Posts( img=data['img_url'], caption=data['caption'], location=data['location'], user_id=data['user_id'])
    new_post.save()
    return jsonify({
        'status': 'ok',
        'message': 'Post successfully created'
    })