# import mysql.connector
# from mysql.connector import Error
# import pandas as pd
import mysql
from mysql.connector.errors import Error


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


create_clothing_table = """
CREATE TABLE clothing (
  clothing_id INT NOT NULL,
  color VARCHAR(40) NOT NULL,
  type VARCHAR(40) NOT NULL,
  seasons VARCHAR(40) NOT NULL,
  size VARCHAR(3),
  last_worn DATE,
  is_clean INT,
  stored_in VARCHAR(40), 
  pic_file_name VARCHAR(200),
  PRIMARY KEY (clothing_id),
  FOREIGN KEY (stored_in) REFERENCES storageunit(name)
  );
 """


create_storage_unit_table = """
CREATE TABLE storageunit (
  name VARCHAR(40) NOT NULL,
  location VARCHAR(40),
  maxcapacity INT,
  currentcapacity INT,
  PRIMARY KEY (name),
  CHECK (currentcapacity<=maxcapacity)
  );
 """


drop_clothing_table = """
DROP TABLE clothing;
 """


drop_storage_unit_table = """
DROP TABLE storageunit;
 """


pop_storage = """
INSERT INTO storageunit VALUES
('closet', 'home', 100, 0),
('drawers', 'home', 200, 0), 
('box 1 under bed', 'home', 50, 0);
"""


# code used to setup db

# test_connection = create_server_connection("localhost", "root", "megan123")
# create_closet_query = "CREATE DATABASE closet"
# create_database(test_connection, create_closet_query)
connection = create_db_connection("localhost", "root", "megan123", "closet")
execute_query(connection, drop_clothing_table)
execute_query(connection, drop_storage_unit_table)
execute_query(connection, create_storage_unit_table)
execute_query(connection, create_clothing_table)
execute_query(connection, pop_storage)
