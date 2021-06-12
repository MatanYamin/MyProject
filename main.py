# By Matan Yamin - MyProject

from flask import Flask, request
import flask
import db_connection as connect  # the connection to the DB
import handle_requests as handle  # the place where all the functions at
import config

app = Flask(__name__)


# Here we are creating a new message as requested.
@app.route("/write_message", methods=["POST"])
def write_message():
    """This method gets parameters for a message and adds to the DB"""
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    data = request.get_json(force=True)  # fetching data from the request
    temp = handle.add_message_to_db(cursor, connection, data)  # sending data to the handler
    connection.close()  # close connection to avoid overload
    if temp == 0:
        return "One of the fields is incorrect or missing."
    return "Your message to '" + data['Receiver'] + "' has been sent successfully."


# Here we are getting a name (User) and returning all of his messages.
@app.route("/messages_for_user", methods=["GET"])
def read_messages_for_user():
    # Connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    data = request.get_json(force=True)  # Fetching data from the request
    # Sending data to the handler and receive all the messages inside a list called "messages":
    messages = handle.read_messages_for_specific_user(cursor, connection, data['User'])
    connection.close()  # Close connection to avoid overload
    return flask.jsonify(messages)


# Here we are getting a name (User) and returning all unread messages he has.
@app.route("/unread_messages_for_user", methods=["GET"])
def unread_messages_for_user():
    # Connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    data = request.get_json(force=True)  # Fetching data from the request
    # Sending data to the handler and receive all unread messages inside a list called "unread_messages":
    unread_messages = handle.get_unread_messages_for_specific_user(cursor, connection, data['User'])
    connection.close()  # Close connection to avoid overload
    return flask.jsonify(unread_messages)


# Here we are getting a message's Id and returning the same message.
@app.route("/read_message", methods=["GET"])
def read_single_message():
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    data = request.get_json(force=True)  # fetching data from the request
    # sending the Id num to the handler and receive the specific message:
    single_message = handle.read_single_message(cursor, connection, data['Id'])
    connection.close()  # close connection to avoid overload
    if not single_message:
        return "There is no message with such Id."
    return flask.jsonify(single_message)


# here we are getting a message's Id and deleting it from the DB.
@app.route("/delete_message", methods=["DELETE"])
def delete_message():
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    data = request.get_json(force=True)  # fetching data from the request
    # sending the Id num to the handler inorder to delete the specific message:
    handle.delete_single_message(cursor, connection, data['Id'])
    connection.close()  # close connection to avoid overload
    return "The message has been deleted successfully."


# in "login" we receive username and password from Postman "Basic Auth", verify and then returning all his messages
@app.route("/login", methods=["GET"])
def login_to_read_messages():
    user = request.authorization["username"]
    password = request.authorization["password"]
    if not user or not password:
        return "Username and/or Password is missing."
    if password == config.temp_password():
        # connection to DB
        connection = connect.connect_db()
        cursor = connection.cursor()
        # sending the username inorder to get all of his messages:
        messages = handle.get_messages_for_logged_user(cursor, connection, user)
        connection.close()  # close connection to avoid overload
        return flask.jsonify(messages)
    else:
        return "Wrong password."


@app.route("/check", methods=["GET"])
def get_something():
    return "Check works"


if __name__ == "__main__":
    app.run(debug=True)