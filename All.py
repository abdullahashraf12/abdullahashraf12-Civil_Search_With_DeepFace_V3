from sys import path
import PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from mysql.connector import errors
from mysql.connector.errors import Error, IntegrityError
from MainWindow import Ui_My_App
from PySide6 import QtWidgets
import mysql.connector as mysqlcon
import os
import shutil
from deepface import DeepFace
import time
from PySide6.QtCore import QThread
from numba import jit,cuda

class MainWindow(QtWidgets.QMainWindow,Ui_My_App):

    def __init__(self,path_image):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.upload_photo_button.clicked.connect(self.upload_photo_dialog)
        self.insert_data_button.clicked.connect(self.insert_data)
        self.search.clicked.connect(self.searching_by_ssn)
        self.delete_submit_button.clicked.connect(self.delete_by_ssn)
        self.modify_button.clicked.connect(self.modify)
        self.__path_image=path_image
        self.upload_photo_button_s.clicked.connect(self.get_details_search_button_function)
        self.pushButton.clicked.connect(self.search_by_face)
        self.show()
    # getter method
    def get_path_image(self):
        return self.__path_image
      
    # setter method
    def set_path_image(self, x):
        self.__path_image = x
        
    def get_path_image_search(self):
        if(self.__path_image==None or self.__path_image==""):
            msg=QtWidgets.QMessageBox()
            msg.setGeometry(1000,500,500,350)
            msg.setText("Please Enter Photo to Search for")
            msg.exec()
        return self.__path_image
      
    # setter method
    def set_path_image_search(self, x):
        self.__image_path = x
    


    def social_stat_modify(self):
        social_state=str(self.social_state_modify.currentText())
        return social_state

    def get_name(self):
        first_name=str(self.first_name.text())    
        second_name=str(self.second_name.text())    
        full_name=str(self.full_name.text())    
        dictionary_full_name={"first_name":first_name,"second_name":second_name,"full_name":full_name}
        return dictionary_full_name
    
    
    def get_data_type_of_click_birth(self):
        day=self.date_of_birth.date().day()
        month=self.date_of_birth.date().month()
        year=self.date_of_birth.date().year()
        dictionary_birth_date={"day":day,"month":month,"year":year}
        return dictionary_birth_date

    def get_gender_type(self):
        gender_type=str(self.gender_type.currentText())
        return gender_type

    def get_social_state(self):
        social_state=str(self.socia_state.currentText())
        return social_state

    def get_address(self):
        address=str(self.address.text())
        return address
    def get_image_unique(self):
        image_unique_code=str(self.image_uniqe_code.text())
        return image_unique_code

    def get_ssn(self):
            ssn=str(self.social_security_number.text())
            return ssn

    def upload_photo_dialog(self):

            
        file_name_and_directory,thing=QtWidgets.QFileDialog.getOpenFileName(self,"open person photo","/home/abdo_ashraf/")
        label = self.image_person
        my_photo=QPixmap(file_name_and_directory)
        my_photo_size=my_photo.scaled(620,310,Qt.KeepAspectRatio,Qt.FastTransformation)
        label.setPixmap(my_photo_size)
        self.set_path_image(file_name_and_directory)
       
        


    def error(self,err):
        a=str(err)
        if a.startswith("1062 (23000): Duplicate entry") == True:
            err_msg=QtWidgets.QMessageBox()
            err_msg.setGeometry(1000,500,500,350)
            err_msg.setText("Duplicate Value")
            err_msg.exec()
        elif(a.startswith("FileNotFoundError: [Errno 2] No such file or directory")):
            err_msg=QtWidgets.QMessageBox()
            err_msg.setGeometry(1000,500,500,350)
            err_msg.setText("Photo not in Directory Please enter Photo")
            err_msg.exec()
            self.upload_photo_dialog()
        elif(a.startswith("ValueError: substring not found")):
            err_msg=QtWidgets.QMessageBox()
            err_msg.setGeometry(1000,500,500,350)
            err_msg.setText("Error In Path")
            err_msg.exec()
            self.upload_photo_dialog()
        elif (a.startswith("substring not found")):
            err_msg=QtWidgets.QMessageBox()
            err_msg.setGeometry(1000,500,500,350)
            err_msg.setText(a+" Please Enter Photo It's Must")
            err_msg.exec()
            self.upload_photo_dialog()


    # @jit(target_backend="cuda")
    def search_by_face(self):
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
        result={"verified":None}
        connection2 = mysqlcon.connect(
            user='abdo', 
            password='01123119835',
            host='127.0.0.1',
            database='civil_db')
        cursor2 = connection2.cursor(buffered=True)

        sql_2="SELECT COUNT(*) FROM civilization_table"
        cursor2.execute(sql_2)
        connection2.commit()  
        record2 = cursor2.fetchall()
        cursor2.close()
        connection2.close()
        number=0
        for i in record2:
            number=int(str(i).replace("(","").replace(")","").replace(",",""))

        i=1
        start_time = time.time()

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
            
            # type_of_image=row[12]
          
            # try:
            result = DeepFace.verify(img1_path = self.get_path_image_search() , 
            img2_path = person_image_data, 
            model_name = models[7],
            detector_backend=backends[2]
            )
            if(result["verified"]==True and i<=number):                
                self.first_name_text_2.setText(first_name)
                self.second_name_text_2.setText(second_name)
                self.full_name_text_2.setText(full_name)
                self.dob_text_2.setText("Day: {} , Month: {} , Year: {}".format(str(day_birth),str(month_birth),str(year_birth)))
                self.gender_text_2.setText(gender_type)
                self.full_address_text_2.setText(address)
                self.uic_text_3.setText(ssn)
                self.uic_text_2.setText(uic)
                label=self.recognised_image
                my_photo=QPixmap(person_image_data)
                my_photo_size=my_photo.scaled(620,310,Qt.KeepAspectRatio,Qt.FastTransformation)
                label.setPixmap(my_photo_size)
                self.social_state_text_2.setText(social_state_text)
                self.label_15.setText("Found")
                self.label_11.setText("Verified")
                self.label_11.setStyleSheet("QLabel { background-color : black; color : green; }")
                self.repaint()
                break
                # self.label_11.show()
                # print("--- %s seconds ---" % (time.time() - start_time))
                # break
       
                

                
                            
                
                
        

            elif(result["verified"]==False and i<number):
                self.label_15.setText("Processing")
                self.label_15.setStyleSheet(" background-color :white ; color : green;")
                self.label_11.setStyleSheet("QLabel { background-color : black; color : red; }")
                self.label_11.show()
                label=self.recognised_image
                my_photo=QPixmap(person_image_data)
                my_photo_size=my_photo.scaled(620,310,Qt.KeepAspectRatio,Qt.FastTransformation)
                label.setPixmap(my_photo_size)
                self.label_11.setText("Searching...")
                self.label_15.repaint()
                
        
            elif(result["verified"]==False and i==number):
                self.first_name_text_2.setText("Null")
                self.second_name_text_2.setText("Null")
                self.full_name_text_2.setText("Null")
                self.dob_text_2.setText("Null")
                self.gender_text_2.setText("Null")
                self.full_address_text_2.setText("Null")
                self.social_state_text_2.setText("Null")
                self.uic_text_2.setText("Null")
                label=self.recognised_image
                label.setText("Null")
                self.social_state_text_2.setText("Null")
                self.label_15.setText("No Data is Found")
                self.uic_text_3.setText("Null")
                self.label_11.setText("Person isn't in DB")
                self.label_11.setStyleSheet("QLabel { background-color : black; color : red; }")
                self.repaint()
            i+=1



        # except Exception as e:
        #     if (str(e)=="Face could not be detected. Please confirm that the picture is a face photo or consider to set enforce_detection param to False."):
        #         self.label_15.setText("face couldn't be found")
        #         self.label_11.hide()
        #         break
        #     else:
        #         print(str(e))
        #         msg=QtWidgets.QMessageBox()
        #         msg.setGeometry(1000,500,500,350)
        #         self.first_name_text_2.setText("Null")
        #         self.second_name_text_2.setText("Null")
        #         self.full_name_text_2.setText("Null")
        #         self.dob_text_2.setText("Null")
        #         self.gender_text_2.setText("Null")
        #         self.full_address_text_2.setText("Null")
        #         self.social_state_text_2.setText("Null")
        #         self.uic_text_2.setText("Null")
        #         label=self.recognised_image
        #         label.setText("Null")
        #         self.social_state_text_2.setText("Null")
        #         self.label_15.setText("No Data is Found")
        #         self.uic_text_3.setText("Null")
        #         msg.setText("Please Enter Photo")
        #         msg.exec()
        #         self.label_11.setText("")
        #         self.label_11.hide()
        #         break






    def insert_data(self):
        
        msg=QtWidgets.QMessageBox()
        msg.setGeometry(1000,500,500,350)
        connection = mysqlcon.connect(
            user='abdo', 
            password='01123119835',
            host='127.0.0.1',
            database='civil_db')
            
        try:
            path=str(self.get_path_image())
            dot = "."
            new_extention=path[path.index(dot) + len(dot):]
            if self.get_name().get("first_name") == "" or self.get_name().get("second_name") == "" or self.get_name().get("full_name") == "" or  self.get_address() == "" or self.get_ssn() == "" or self.get_image_unique() == ""  :
                
                msg.setText("Please Enter Data")
                msg.exec()
            
            else:

                if path == "None":
                    msg.setText("Please Enter Photo")
                    msg.setStandardButtons(msg.Ok)
                    msg.exec()
                elif path !="None":
                    f= open(path, 'rb')
                    binaried_image= f.read()                
                cursors = connection.cursor(buffered=True)
                print("Hello World")
                sql_statement="INSERT INTO civilization_table (first_name,second_name,full_name,day_birth,month_birth,year_birth,gender_type,address,ssn,unique_code_image,person_image,social_state,type_of_image) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                result=cursors.execute(sql_statement,(self.get_name().get("first_name"),self.get_name().get("second_name"),self.get_name().get("full_name"),self.get_data_type_of_click_birth().get("day"),self.get_data_type_of_click_birth().get("month"),self.get_data_type_of_click_birth().get("year"),self.get_gender_type(),self.get_address(),self.get_ssn(),self.get_image_unique(),self.get_path_image(),str(self.get_social_state()),str(new_extention)))
                connection.commit()
                print(result)
                if result == None:
                    msg.setText("Data Inserted Successfully")
                    msg.exec()
                elif result != None:
                    msg.setText(result)
                    msg.exec()
                else:
                    msg.setText("error")
                    msg.exec()
            # except mysqlcon.Error as err:
            #     self.error(err)
        except mysqlcon.errors.IntegrityError as integ_error:
            self.error(integ_error)
        except FileNotFoundError as f_n_f:
            self.error(f_n_f)
        except ValueError as val_err:
            self.error(val_err)

    def writing_blob_data(self,image_binary_data,ssn,type_of_image):
        blob_file=open("{}".format(ssn)+".{}".format(type_of_image),"wb")
        blob_file.write(image_binary_data)
        blob_file.flush()
        blob_file.close()

    def searching_by_ssn(self):
        msg=QtWidgets.QMessageBox()
        msg.setGeometry(1000,500,500,350)        
        connection = mysqlcon.connect(
            user='abdo', 
            password='01123119835',
            host='127.0.0.1',
            database='civil_db')


        cursor = connection.cursor(buffered=True)

     
        sql_fetch_blob_query = "SELECT * FROM civilization_table where ssn =%s"
        if self.social_security_number_searc_ssn.text() != None or self.social_security_number_searc_ssn.text() != "None" or self.social_security_number_searc_ssn.text()!=None:
            cursor.execute(sql_fetch_blob_query, (self.social_security_number_searc_ssn.text(),))
            connection.commit()
            record = cursor.fetchall()
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
                # type_of_image=row[12]
            if ssn == None or ssn=="None"or ssn=="":
                msg.setText("Please Enter valid ssn if it's valid then it's not in database")
                msg.exec()
            else:
                self.first_name_text.setText(first_name)
                self.second_name_text.setText(second_name)
                self.full_name_text.setText(full_name)
                self.dob_text.setText("Day :- "+str(day_birth)+" Month:- "+str(month_birth)+" Year:- "+str(year_birth))
                self.gender_text.setText(gender_type)
                self.social_state_text.setText(social_state_text)
                self.full_address_text.setText(address)
                self.uic_text.setText(uic)

                file_name_and_directory=person_image_data
                print(file_name_and_directory)
                label = self.Photo_Label
                my_photo=QPixmap(file_name_and_directory)
                my_photo_size=my_photo.scaled(620,310,Qt.KeepAspectRatio,Qt.FastTransformation)
                label.setPixmap(my_photo_size)
                self.set_path_image(person_image_data)


                msg.setText("Successfully Returned Data")
                msg.exec()


    def delete_by_ssn(self):

        
        msg=QtWidgets.QMessageBox()
        msg.setGeometry(1000,500,500,350) 
        connection = mysqlcon.connect(
            user='abdo', 
            password='01123119835',
            host='127.0.0.1',
            database='civil_db')
        cursor = connection.cursor(buffered=True)


        sql_fetch_blob_query_select = "SELECT ssn FROM civilization_table where ssn = %s"
        cursor.execute(sql_fetch_blob_query_select, (self.social_security_number_delete.text(),))
        connection.commit()
        record = cursor.fetchall()
        ssn=""
        for row in record:
            ssn=row[0]

        if ssn == None or ssn=="None" or ssn=="":
            msg.setText("Please Enter valid ssn if it's valid then it's not in database")
            msg.exec()
        else:
            sql_fetch_blob_query_2 = "DELETE FROM civilization_table WHERE ssn =%s"
            cursor = connection.cursor()
            cursor.execute(sql_fetch_blob_query_2, (self.social_security_number_delete.text(),))
            connection.commit()
            msg.setText("Record Deleted Sucessfully")
            msg.exec()
    






    def modify(self):
        msg=QtWidgets.QMessageBox()
        msg.setGeometry(1000,500,500,350) 
        connection = mysqlcon.connect(
            user='abdo', 
            password='01123119835',
            host='127.0.0.1',
            database='civil_db')
        cursor = connection.cursor(buffered=True)


        sql_fetch_blob_query_select = "SELECT ssn FROM civilization_table where ssn = %s"
        cursor.execute(sql_fetch_blob_query_select, (self.social_security_number_modify.text(),))
        connection.commit()
        record = cursor.fetchall()
        ssn=""
        for row in record:
            ssn=row[0]

        if ssn == None or ssn=="None" or ssn=="":
            msg.setText("Please Enter valid ssn if it's valid then it's not in database")
            msg.exec()
        else:
            msg.setText("found ssn please modify Wait For Modifying")
            msg.exec()

            sql_fetch_blob_query_2 = "UPDATE civilization_table SET social_state=%s WHERE ssn= %s"
            cursor = connection.cursor()
            cursor.execute(sql_fetch_blob_query_2, (self.social_stat_modify(),self.social_security_number_modify.text(),))
            connection.commit()
            msg.setText("Record Modified Sucessfully")
            msg.exec()


    def uploaded_image_search_by_image(self):
        file_name_and_directory,thing=QtWidgets.QFileDialog.getOpenFileName(self,"open person photo","/home/abdo_ashraf/")
        
        label = self.uploaded_image
        my_photo=QPixmap(file_name_and_directory)
        my_photo_size=my_photo.scaled(620,310,Qt.KeepAspectRatio,Qt.FastTransformation)
        label.setPixmap(my_photo_size)
        self.set_path_image(file_name_and_directory)
        path=file_name_and_directory
        self.set_path_image_search(path)



    def get_details_search_button_function(self):
        msg=QtWidgets.QMessageBox()
        msg.setGeometry(1000,500,500,350)
        # msg.setText("Please Enter Photo")
        # msg.exec()
        file=self.uploaded_image_search_by_image()


        if file!= None or file != "None" or file != "":

            msg=QtWidgets.QMessageBox()
            msg.setGeometry(1000,500,500,350) 
            connection = mysqlcon.connect(
            user='abdo', 
            password='01123119835',
            host='127.0.0.1',
            database='civil_db')
            cursor = connection.cursor(buffered=True)


            sql_fetch_blob_query_select = "SELECT ssn,person_image,type_of_image FROM civilization_table"
            cursor.execute(sql_fetch_blob_query_select)
            connection.commit()
            record = cursor.fetchall()
            ssn=""
            person_image=None
            type_of_image=""
            for row in record:
                ssn=row[0]
                person_image=row[1]
                type_of_image=row[2]
                
          
        else:
            msg.setText("Please Enter Photo")
            msg.exec()

    def database_general(self):
        path="C:/Users/alpha/OneDrive/Desktop/Database Project/Data_Base_Project/image_to_find"
        if not os.path.exists(path):
            os.mkdir(path)
            print("/home/abdo_ashraf/Data_Base_Project/" , "All_photos" ,  " Created ")
        else:    
            print("Already Exists")
        return path

    def inputted_image_in_db_fiolder(self):
        path="C:/Users/alpha/OneDrive/Desktop/Database Project/Data_Base_Project/image_to_find"
        if not os.path.exists(path):
            os.mkdir(path)
        else:    
            print("Already Exists")
        return path

    def folder_for_all_photos_retreived(self):
        path="C:/Users/alpha/OneDrive/Desktop/Database Project/Data_Base_Project/image_to_find"
        if not os.path.exists(path):
            os.mkdir(path)
            print("/home/abdo_ashraf/Data_Base_Project/" , "All_photos" ,  " Created ")
        else:    
            print("Already Exists")
        return path
    def full_path_files_searched_in_database(self):
        path=self.inputted_image_in_db_fiolder()
        return path
 
    def Copying_inputted_image_to_spescified_folder(self,path):
        self.database_general()
        self.inputted_image_in_db_fiolder()
        self.folder_for_all_photos_retreived()
        path_image=self.get_path_image_search()
        dot = "."
        extention=path_image[path_image.index(dot) + len(dot):]

        print(path)
        src_path = path_image
        dst_path = self.full_path_files_searched_in_database()+"/{}".format(os.path.basename(path_image))+".{}".format(extention)
        print(src_path)
        print(dst_path)
        shutil.copy(src_path, dst_path)
        
    # def writing_image_retreived_from_db(self,ssn,person_image,type_of_image):
    #     self.database_general()
    #     self.folder_for_all_photos_retreived()
    #     msg=QtWidgets.QMessageBox()
    #     msg.setGeometry(1000,500,500,350)

    #     path1=self.get_path_image_search()
    #     self.Copying_inputted_image_to_spescified_folder(path1) 

    #     path2=self.folder_for_all_photos_retreived()
    #     file=open("{}/{}.{}".format(str(path2),str(ssn),str(type_of_image)),"wb")
    #     file.write(bytes(person_image))
    #     file.flush()
    #     file.close()