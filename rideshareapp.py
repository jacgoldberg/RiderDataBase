from asyncio.windows_events import NULL
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="Password1",
                               auth_plugin='mysql_native_password', database="RideShare")
print(mydb)
mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS user (userID SMALLINT, userRating DECIMAL(3,2),name VARCHAR(15), status VARCHAR(15), PRIMARY KEY(userID));")
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS driver (driverID SMALLINT, driverRating DECIMAL(3,2), name VARCHAR(15), totalRides SMALLINT, status VARCHAR(15), PRIMARY KEY(driverID));")
mycursor.execute("CREATE TABLE IF NOT EXISTS rides (rideID SMALLINT, price DECIMAL(3, 2), userID SMALLINT, date DATE, time TIME, driverID SMALLINT, startLocation VARCHAR(15), endLocation VARCHAR(15), status VARCHAR(15), PRIMARY KEY(rideID), FOREIGN KEY(userID) REFERENCES user(userID), FOREIGN KEY(driverID) REFERENCES driver(driverID));")


class User:
    def __init__(self, id, name, status):
        self.userID = id
        self.userName = name
        self.userStatus = status
class Driver:
    def __init__(self, id, rating, name, totRides):
            self.driverID = id
            self.driverRating = rating
            self.name = name
            self .totalRides = totRides
def changeRiderStatus(userID, setToAV):
    if(setToAV):
        mycursor.execute(f"UPDATE driver SET status = 'available' WHERE driverID = {userID}")
    else:
        mycursor.execute(f"UPDATE driver SET status = 'unavailable' WHERE driverID = {userID}")
    #query = mycursor.execute(f"SELECT status FROM driver WHERE driverID = {userID}")
    #q = mycursor.fetchall()
    #print(q)
    return 1

def logIn(username, userID):
    # check to see if the user's name and id are stored in the db
    #mycursor.execute("SELECT userID, name FROM user WHERE")
    query1 = mycursor.execute(f"SELECT driverID FROM driver WHERE driverID = {userID}")
    q = mycursor.fetchall()
   
    print(q)
    if(len(q) != 0):
        dbID = int(q[0][0])
        print(dbID)
        if(int(userID) == dbID):
            print("User matched to driver")
            query2 = mycursor.execute(f"SELECT name FROM driver WHERE driverID = {userID}")
            q2 = mycursor.fetchall()
            dbName = q2[0][0]
            print(dbName)
            if(username == dbName):
                print("Matched")
                #function call
                return 1
    else:
        query3 = mycursor.execute(f"SELECT userID FROM user WHERE userID = {userID}")
        q3 = mycursor.fetchall()
        dbID = int(q3[0][0])
        print("UserID: " + str(dbID))
        if(int(userID) == dbID):
            query4 = mycursor.execute(f"SELECT name FROM user WHERE userID = {userID}")
            q4 = mycursor.fetchall()
            dbName = q4[0][0]
            print("User Name: " + dbName)
            if(username == dbName):
                #some function
                return 0

        else:
            print("Invalid login")
    return 1


def main():
    print("Hello welcome to the rideshare app")
    username = input("Please enter your name: ")
    userID = input("Please enter your User ID number: ")
    userType = logIn(username, userID)
    while(1):
        if(userType):
            tempStr = input("Would you like to change your status?(Y/n): ")
            if(tempStr == "Y"):
                changeRiderStatus(userID, 1)
            else:
                if(tempStr == "n"):
                    changeRiderStatus(userID, 0)
                else:
                    print("Did not enter character correctly")
            print("Searching for rider...")
            return 1
        
        


if __name__ == "__main__":
    main()



mydb.close()
