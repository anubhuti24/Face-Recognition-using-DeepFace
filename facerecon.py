from sqlite3 import Cursor
from urllib import response
from deepface import DeepFace

import mysql.connector
from mysql.connector import Error
from numpy import imag

def create_server_connection(host_name, user_name, passwd, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=passwd,
            auth_plugin='mysql_native_password',
            database=db_name
        )
    except Error as err:
        print(f"Error: '{err}'")

    return connection

inimg = input("Enter image name: ")
in_img = "input_images/" + inimg
model = "Facenet"
validity = False

connection = create_server_connection("localhost", "root", "password", "MNREGA")
mycursor = connection.cursor()

mycursor.execute("SELECT COUNT(*) FROM worker;")
total_workers = int(mycursor.fetchall()[0][0]);

mycursor.execute("SELECT * FROM worker;")
data = mycursor.fetchall();

for i in range(0, total_workers):
    worker_name = data[i][0]
    worker_img = data[i][1]

    response = DeepFace.verify(img1_path=in_img, img2_path=worker_img, model_name=model)
    
    validity = bool(response["verified"])

    if validity == True:
        print("Match Found =", worker_name)
        mycursor.execute("UPDATE worker SET attendance=attendance+1 WHERE name='{}';".format(worker_name))
        connection.commit();
        break

if validity == False:
    print("No match found in the database")

mycursor.close()