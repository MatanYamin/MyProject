# By Matan Yamin - MyProject


def add_message_to_db(cursor, mydb, data):
    """The function 'add_message_to_db' get message's data containing:
    1) Sender
    2) Receiver
    3) Message
    4) Subject
    5) Creation date."""
    if check_values(data) == 0:
        # If the return is 0, it means something is missing.
        return 0
    sql = "INSERT INTO messages (Sender, Receiver, Message, Subject, Date, Unread) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (data['Sender'], data['Receiver'], data['Message'], data['Subject'], data['Date'], "0")
    cursor.execute(sql, val)
    mydb.commit()
    return 1


def read_messages_for_specific_user(cursor, mydb, user):
    """The function 'read_messages_for_specific_user' gets receiver's name and returns all his messages."""
    cursor.execute("SELECT * FROM messages WHERE Receiver = %s", (user,))
    messages_list = []
    for message in cursor.fetchall():
        # the '-1' is to avoid getting the last field (Unread). We don't need it here.
        messages_list.append(message[:-1])
    # Sending the messages we just fetched and mark them as 'read'.
    mark_message_as_read(cursor, messages_list)
    mydb.commit()
    return messages_list


def get_unread_messages_for_specific_user(cursor, mydb, user):
    """The function 'get_unread_messages_for_specific_user' gets a user name and returning all his unread messages.
       After getting those messages, the field "Unread" is updated to 1.
       0 inside 'Unread' means that a message has not been read yet."""
    cursor.execute("SELECT * FROM messages WHERE Receiver = %s AND Unread = %s", (user, "0", ))
    messages_list = []
    for message in cursor.fetchall():
        # the '-1' is to avoid getting the last field (Unread). We don't need it here.
        messages_list.append(message[:-1])
    # Sending the messages we just fetched and mark them as 'read'.
    mark_message_as_read(cursor, messages_list)
    mydb.commit()
    return messages_list


def read_single_message(cursor, mydb, id):
    """The function 'read_single_message' gets message's Id and returns the very same message
       with the same Id."""
    cursor.execute("SELECT * FROM messages WHERE ID = %s ", (id,))
    messages_list = []
    for message in cursor.fetchall():
        # the '-1' is to avoid getting the last field (Unread). We don't need it here.
        messages_list.append(message[:-1])
    # Mark that message as read.
    mark_message_as_read(cursor, messages_list)
    mydb.commit()
    return messages_list


def delete_single_message(cursor, mydb, id):
    """The function 'delete_single_message' gets message's Id and deletes it from DB."""
    # a Simple delete query.
    sql = "DELETE FROM messages WHERE ID = %s"
    val = (id,)
    cursor.execute(sql, val)
    mydb.commit()


def mark_message_as_read(cursor, messages):
    """The function 'mark_message_as_read' gets a list of messages (or 1 message) and marks them as 'read'.
       The function finds the unique ID of a message and marks the field "unread" as 1.
       When the field is 0 it means the message has not been read yet."""
    for flag in messages:
        sql = "UPDATE messages SET Unread = %s WHERE ID = %s"
        val = ("1", flag[0], )
        # "flag[0]" is the "ID" field of a message
        cursor.execute(sql, val)


def get_messages_for_logged_user(cursor, mydb, user):
    cursor.execute("SELECT * FROM messages WHERE Receiver = %s ", (user,))
    messages_list = []
    for message in cursor.fetchall():
        # the '-1' is to avoid getting the last field (Unread). We don't need it here.
        messages_list.append(message[:-1])
    # Mark that message as read.
    mark_message_as_read(cursor, messages_list)
    mydb.commit()
    return messages_list


def check_values(data):
    """This function just checking the body of the request."""
    try:
        if data['Sender'] and data['Receiver'] and data['Message'] and data['Subject'] and data['Date']:
            return 1
    except:
        return 0