import json
from flask import Flask, request
import db
DB = db.DatabaseDriver()


app = Flask(__name__)


@app.route("/")
@app.route("/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return json.dumps({"users": DB.get_all_users()}), 200



@app.route("/users/", methods = ["POST"])
def create_users():
    """
    Endpoint for creating a new user
    """

    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance",0)
    if balance is None:
        balance = 0
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    print(name)
    print(name)
    if user is None:
        return json.dumps({"error": "Something went wrong while making user"}), 400
    return json.dumps(user), 201



@app.route("/users/<int:user_id>/")
def get_task(user_id):
    """
    Endpoint for getting a user by ID
    """
    
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found!"}), 404
    return json.dumps(user), 200
 

@app.route("/users/<int:user_id>", methods = ["POST"])
def update_user(user_id):
    """
    Endpoint for updating a user by ID
    """

    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance")
    
    DB.update_user_by_id(user_id, name, username, balance)

    task = DB.get_user_by_id(user_id)
    if task is None:
        return json.dumps({"error": "User not found!"}), 404
    return json.dumps(task), 200 


@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
       return json.dumps({"error": "User not found!"}), 404 
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200


@app.route("/send/", methods=["POST"])
def transfer_user():
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    if sender_id is None and receiver_id is None and amount is None:
       return json.dumps({"error": "No Information Provided!"}), 400
    if sender_id is None and receiver_id is None:
       return json.dumps({"error": "No Sender or Receiver Provided!"}), 400
    if receiver_id is None and amount is None:
       return json.dumps({"error": "No Receiver or amount Provided!"}), 400
    if sender_id is None and amount is None:
       return json.dumps({"error": "No Sender or Amount Provided!"}), 400
    if sender_id is None:
       return json.dumps({"error": "No Sender Provided!"}), 400
    if receiver_id is None:
       return json.dumps({"error": "No Receiver Provided!"}), 400
    if amount is None:
       return json.dumps({"error": "No Amount Provided!"}), 400
    
    balance_sender = DB.get_user_by_id(sender_id).get("balance")
    balance_reciever = DB.get_user_by_id(receiver_id).get("balance")
    name_sender = DB.get_user_by_id(sender_id).get("name")
    name_reciever = DB.get_user_by_id(receiver_id).get("name")
    username_sender = DB.get_user_by_id(sender_id).get("username")
    username_reciever = DB.get_user_by_id(receiver_id).get("username")
    if  balance_sender < amount:
       return json.dumps({"error": "Balance not enough!"}), 400
    updated_sender = balance_sender - amount
    updated_reciever =balance_reciever + amount
    DB.update_user_by_id(sender_id, name_sender, username_sender, updated_sender)
    DB.update_user_by_id(receiver_id, name_reciever, username_reciever, updated_reciever)
    return json.dumps(body), 200

# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
