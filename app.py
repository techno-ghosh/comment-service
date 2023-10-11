from flask import Flask, request ,jsonify
import requests

app = Flask(__name__)

comments = {
        '1': {'user_id': '1', 'post_id': '1', "comment" : 'This is first comment'},
        '2': {'user_id': '2', 'post_id': '2', "comment" : "This is the second comment"}
    }

@app.route('/')
def hello():
    return comments


# READ OPERATION

@app.route('/comments/<id>')
def post(id):
   
    comment_info = comments.get(id, {})
    
    # Get user info from User Service
    if comment_info:
        
        post_response = requests.get(f'https://postservicewebappversiontwo.azurewebsites.net/post/{comment_info["post_id"]}')
        if post_response.status_code == 200:
            comment_info['post'] = post_response.json()
        else:
            comment_info['post_response'] = post_response.status_code
            
        user_response = requests.get(f'https://postservicewebappversiontwo.azurewebsites.net/user/{comment_info["user_id"]}')
        if user_response.status_code == 200:
            comment_info['user'] = user_response.json()
        else:
            comment_info['user_response'] = user_response.status_code

    return jsonify(comment_info)


# CREATE OPERATION
@app.route('/comments/add',methods=['POST'])
def create():
    post_id = request.json['post_id']
    user_id = request.json['user_id']
    comment = request.json['comment']
    response = requests.get(f'https://postservicewebappversiontwo.azurewebsites.net/post/{post_id}')
    
    if response.status_code != 200:
        return 'Post not found',404
    
    user_response = requests.get(f'https://webappsfromlocalnirmalghosh.azurewebsites.net/user/{user_id}')
    
    if user_response.status_code != 200:
        return 'User not found',404
    
    new_key = int(sorted(comments.keys())[-1]) + 1

    comments[f'{new_key}'] = {
        "user_id" : user_id,
        "post_id" : post_id,
        "comment" : comment
    }
    return jsonify(comments)


# UPDATE OPERATION
@app.route('/comments/update_comment', methods=['PUT', 'POST'])
def update():
    if(request.method == 'POST' or request.method == 'PUT'):
        
        if(comments.get(str(request.json['id']), {})):
        
            comment = request.json['comment']
            comment_id = request.json['id']
            print(comments[f'{comment_id}'])
            comments[f'{comment_id}'] = {
                "user_id" : comments[f'{comment_id}']['user_id'],
                "comment" : comment,
                "post_id" : comments[f'{comment_id}']['post_id'],
            }
            return comments[f'{comment_id}']
        else: 
            return "comment not found"
    else:
        return 'method not allowed',403

# DELETE OPERATION

@app.route('/comments/delete_comment', methods=['DELETE'])
def delete():
    
    if(request.method == 'DELETE'):
        
        if(comments.get(str(request.json['comment_id']), {})):
            
            comments.pop(str(request.json['comment_id']))        
            return {
                "message" : "commment deleted",
                "remaninig_comments" : comments
            }
        else:
            return 'comment does not exist'
    else:
        return 'method not allowed',403



if __name__ == '__main__':
    app.run('0.0.0.0',port=5002)