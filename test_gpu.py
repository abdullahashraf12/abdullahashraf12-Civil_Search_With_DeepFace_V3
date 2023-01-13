from deepface import DeepFace
import time
from PySide6.QtCore import QThread
from numba import jit,cuda
import mysql.connector as mysqlcon

def main():
    connection = mysqlcon.connect(
    user='abdo', 
    password='01123119835',
    host='127.0.0.1',
    database='civil_db')
    cursor = connection.cursor(buffered=True)



    sql_fetch_blob_query = "SELECT * FROM civilization_table"

    cursor.execute(sql_fetch_blob_query)
    connection.commit()
    record = cursor.fetchall()
    cursor.close()
    connection.close()
    
    models = [
    "VGG-Face", # 0
    "Facenet",  # 1
    "Facenet512", # 2
    "OpenFace", # 3
    "DeepFace", # 4
    "DeepID", # 5
    "ArcFace", # 6
    "Dlib", # 7
    #   "SFace", # 8
    ]
    backends = [
    'opencv', # 0
    'ssd', # 1
    'dlib', # 2
    'mtcnn', # 3
    'retinaface', # 4 
    'mediapipe'# 5
    ]
    first_name=""
    second_name=""
    full_name=""
    day_birth=""
    month_birth=""
    year_birth=""
    gender_type=""
    address=""
    ssn=""
    uic=""
    social_state_text=""
    person_image_data=None
    type_of_image=""
    start_time=time.time()
    for row in record:
        first_name=row[0]
        second_name=row[1]
        full_name=row[2]
        day_birth=row[3]
        month_birth=row[4]
        year_birth=row[5]
        gender_type=row[6]
        address=row[7]
        ssn=row[8]
        uic=row[9]
        person_image_data = row[10]
        social_state_text=row[11]
        result = DeepFace.verify(img1_path = "C:/Users/alpha/OneDrive/Desktop/Database Project/Data_Base_Project/image_to_find/Screenshot 2023-01-12 190303.jpg", 
                    img2_path = person_image_data, 
                    model_name = models[7],
                    detector_backend=backends[2]
                    )
        if(result["verified"]==False):
            print("--- %s seconds ---" % (time.time() - start_time))
main()