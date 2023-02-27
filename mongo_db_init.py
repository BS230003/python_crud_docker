
from pymongo import MongoClient
import pprint

#
# Docker runs in different IP address, so you need to have IP identifid and put here 
# monogod service is set to bindIp 0.0.0.0, localhost or 127.0.0.1 will not work
#
client = MongoClient ("mongodb://172.17.0.1:27017") # IP I got on my test docker load.


def readMongoDBRecord (what):
    print ('readRecord: MongoDB connected', client)
    db = client["mydb"] # database
    studentList = db.students # collection

    print ('readRecord: Get Collection: ')

    #one_student = studentList.find_one({"name":what}) # get recor
    #pprint.pprint (one_student)
    #print (one_student['name'])

    ret_students = []
    ret_students = list(studentList.find())  # get all records
    print ('got all students')

    #for xx in all_students:
    #    ret_students.append (xx)
    #    print (xx)
    
    # client.close ()
    print ('connection not closed MongoList Len= ', len(ret_students) )
    return ret_students

def addMongoDBRecord (name1, mark1):
    print ('add to MongoDB ')

    #client = MongoClient ("mongodb://localhost:27017")
    db = client["mydb"] # database
    studentList = db.students # collection
    #print ('Get Collection: ', studentList)

    one_student = studentList.insert_one({"name":name1, "marks":mark1}) # get recor
    print ('record added ', one_student )
    return

def deleteMongoDBRecord (name1):
    print ('delete from MongoDB ' + name1)

    #client = MongoClient ("mongodb://localhost:27017")
    db = client["mydb"] # database
    studentList = db.students # collection
    #print ('Get Collection: ', studentList)

    one_student = studentList.delete_one({"name":name1}) # get recor
    print ('record deleted ', one_student)
    return

def updateMongoDBRecord (name1, imgDataStr1):
    print ('update MongoDB image for ' + name1)

    #client = MongoClient ("mongodb://localhost:27017")
    db = client["mydb"] # database
    studentList = db.students # collection
    one_student = studentList.update_one({"name":name1}, {"$set" : {"imgDataStr":imgDataStr1}}) # set record new value
    print ('record updated ', one_student.upserted_id)
    return

#readRecord ('AD')
#readRecord ('AK')

# Created by Bahadur Singh singh.bahadur@gmail.com

