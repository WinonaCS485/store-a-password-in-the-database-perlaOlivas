import pymysql.cursors
#from flask import Flask
import hashlib, uuid

#app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='mrbartucz.com',
                             user='dc0758sw',
                             password='73752',
                             db='dc0758sw_pwHash',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#ask user to store username password
username = input("Enter username: ")
password = input("Enter your password: ")

#create salt salt
salt = uuid.uuid4().hex
#add salt to user's password
saltPW = password + str(salt)

#hash from slides
# this is an open-source method to ONE-WAY hash a password
hashed_password = hashlib.sha512((saltPW).encode('utf-8')).hexdigest()

#print("password: " + password)
#print("salt: " + saltPW)
#print("hash: " + hashed_password)
 
      
try:
    #first 'with' adds data to database
    with connection.cursor() as cursor:
        #INSERT as prepared statement
        sql = "INSERT INTO Passwords(User, Password, Salt) VALUES(%s, %s, %s)"
        
        #execute the SQL command
        cursor.execute(sql, (username, hashed_password, salt))
      
        # If you INSERT, UPDATE or CREATE, the connection is not autocommit by default.
        # So you must commit to save your changes. 
        connection.commit()
        
    #second 'with' grabs data from database
    with connection.cursor() as cursor:
        #select as prepared statement:
        sqlSel = "SELECT Password, Salt from Passwords WHERE User LIKE %s "
        # execute the SQL command
        cursor.execute(sqlSel, username)
        
        for row in cursor:
            #print (result)
            dbPassword = row["Password"]
            dbSalt = row["Salt"]
            #print(dbPassword + " " + dbSalt)
        
finally:
    connection.close()
    
#ask the user to enter it
reenterPassword = input("Please re-enter your password: ")

#New hash with re-entered password and salt from database
decodeHash = hashlib.sha512((reenterPassword + dbSalt).encode('utf-8')).hexdigest()

#compare if second hash and first hash match
if decodeHash == hashed_password:
    print("Correct password!")
else:
    print("Incorrect password!")

