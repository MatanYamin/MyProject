# By Matan Yamin - MyProject

from flask import Flask, request
import flask
import db_connection as connect
import handle_requests as handle

app = Flask(__name__)


@app.route("/write_message", methods=["POST"])
def write_message():
    """This method gets parameters for a message and adds to the DB"""
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    # fetching data from the request
    data = request.get_json(force=True)
    # sending data to the handler
    handle.add_message_to_db(cursor, connection, data)
    # close connection to avoid overloading
    connection.close()
    return "Your message has been sent successfully."


@app.route("/messages_for_user", methods=["GET"])
def read_messages_for_user():
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    # fetching data from the request
    data = request.get_json(force=True)
    # sending data to the handler and receive all the messages inside a list
    messages = handle.read_messages_for_specific_user(cursor, connection, data['User'])
    # close connection to avoid overloading
    connection.close()
    return flask.jsonify(messages)


@app.route("/unread_messages_for_user", methods=["GET"])
def unread_messages_for_user():
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    # fetching data from the request
    data = request.get_json(force=True)
    # sending data to the handler and receive all unread messages inside a list
    unread_messages = handle.get_unread_messages_for_specific_user(cursor, connection, data['User'])
    # close connection to avoid overloading
    connection.close()
    return flask.jsonify(unread_messages)


@app.route("/read_message", methods=["GET"])
def read_single_message():
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    # fetching data from the request
    data = request.get_json(force=True)
    # sending the Id num to the handler and receive the specific message
    single_message = handle.read_single_message(cursor, connection, data['Id'])
    # close connection to avoid overloading
    connection.close()
    return flask.jsonify(single_message)


@app.route("/delete_message", methods=["DELETE"])
def delete_message():
    # connection to DB
    connection = connect.connect_db()
    cursor = connection.cursor()
    # fetching data from the request
    data = request.get_json(force=True)
    # sending the Id num to the handler and inorder to delete the specific message
    handle.delete_single_message(cursor, connection, data['Id'])
    # close connection to avoid overloading
    connection.close()
    return "The message has been deleted successfully."


if __name__ == "__main__":
    app.run(debug=True)