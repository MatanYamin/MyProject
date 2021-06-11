# By Matan Yamin - MyProject

import mysql.connector as mysql
import config as cn


def connect_db():
    """all passwords and usernames are imported from ignored file due to security measures"""
    host_ip = cn.db_ip()
    database = cn.db_name()
    user_name = cn.db_user_name()
    password = cn.db_pass()
    # connect to MySQL server
    db_connection = mysql.connect(host=host_ip, database=database, user=user_name, password=password, port=3306)
    return db_connection


if __name__ == '__main__':
    connect_db()
