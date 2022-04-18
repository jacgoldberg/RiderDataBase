from asyncio import sleep
from asyncio.windows_events import NULL
from asyncore import loop
from re import M
import mysql.connector
import random
import time

mydb = mysql.connector.connect(host="localhost", user="root", password="Password1",
                               auth_plugin='mysql_native_password', database="RideShare")
print(mydb)
mycursor = mydb.cursor()
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS user (userID SMALLINT, userRating DECIMAL(3,2),name VARCHAR(15), status VARCHAR(15), PRIMARY KEY(userID));")
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS driver (driverID SMALLINT, driverRating DECIMAL(3,2), name VARCHAR(15), totalRides SMALLINT, status VARCHAR(15), PRIMARY KEY(driverID));")
mycursor.execute("CREATE TABLE IF NOT EXISTS rides (rideID SMALLINT, userID SMALLINT, driverID SMALLINT, startLocation VARCHAR(15), endLocation VARCHAR(15), status VARCHAR(15), PRIMARY KEY(rideID), FOREIGN KEY(userID) REFERENCES user(userID), FOREIGN KEY(driverID) REFERENCES driver(driverID));")


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
def printRide(rideID):
    mycursor.execute(f"SELECT * FROM RIDES WHERE rideID = {rideID}")
    q = mycursor.fetchall()
    print(q)
    return 1
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
   
    if(len(q) != 0):
        dbID = int(q[0][0])
        if(int(userID) == dbID):
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

def changeUserStatus(userID):
    mycursor.execute(
        f"UPDATE user SET status = 'available' WHERE userID = {userID}")
    mydb.commit()
    mycursor.execute(f"SELECT status FROM user WHERE userID = {userID}")
    t = mycursor.fetchall()
    print("User Status changed to " + t[0][0])


def changeUserStatusUnavailable(userID):
    mycursor.execute(
        f"UPDATE user SET status = 'unavailable' WHERE userID = {userID}")
    mydb.commit()
    mycursor.execute(f"SELECT status FROM user WHERE userID = {userID}")
    t = mycursor.fetchall()
    print("User Status changed to " + t[0][0])


def printDriverInfo(driverID):
    mycursor.execute(f"SELECT name, driverRating, totalRides FROM driver WHERE driverID = {driverID}")
    driverInfo = mycursor.fetchall()
    print("Driver Name: " + str(driverInfo[0][0]))
    print("Driver Rating: " + str(driverInfo[0][1]))
    print("Total Rides: " + str(driverInfo[0][2]))


def checkRideStatus(rideID):
    while(True):
        time.sleep(2)
        mydb = mysql.connector.connect(host="localhost", user="root", password="Password1",
                               auth_plugin='mysql_native_password', database="RideShare")
        mycursor = mydb.cursor()
        mycursor.execute(
            f"SELECT status, driverID, userID FROM rides WHERE rideID = {rideID}")
        rideStatus = mycursor.fetchall()
        print(rideStatus)
        print(rideStatus[0][0])
        if (rideStatus[0][0] == 'accepted'):
            print("Driver found.")
            printDriverInfo(int(rideStatus[0][1]))
            return False
        elif (rideStatus[0][0] == 'denied'):
            print("No driver found.")
            changeUserStatusUnavailable(int(rideStatus[0][2]))
        mydb.close()


def checkValidID(id):
    mycursor.execute("SELECT rideID FROM rides")
    rideID = mycursor.fetchall()
    if id in rideID:
        return True
    else:
        return False


def generateID():
    id = random.randrange(1, 999)
    if checkValidID(id) == True:
        generateID()
    return id


def createRide(userID):
    start_location = input("Start Location: ")
    end_location = input("End Location: ")
    rideID = generateID()
    driverID = None
    sql = "INSERT INTO rides(rideID, userID, driverID, startLocation, endLocation, status) VALUES(%s, %s, %s, %s, %s, %s)"
    vals = (rideID, userID, driverID, start_location, end_location, 'pending')
    mycursor.execute(sql, vals)
    mydb.commit()
    return rideID


def rateDriver(rideID):
    mycursor.execute(f"SELECT driverID FROM rides WHERE rideID = {rideID}")
    driverID = mycursor.fetchall()
    mycursor.execute(f"SELECT driverRating, name, totalRides FROM driver WHERE driverID = {driverID[0][0]}")
    driver = mycursor.fetchall()
    driverRating = input(
        "Please rate " + driver[0][1] + " (out of a 5.0 scale): ")
    rating = (((float(driver[0][0]) * float(driver[0][2])) +
              float(driverRating)) / (float(driver[0][2])) + 1)
    mycursor.execute(
        f"UPDATE driver SET driverRating = {rating} WHERE driverID = {int(driverID[0][0])}")
    mydb.commit()


sql = "UPDATE driver SET totalRides = 4 WHERE driverID = '1024'"
mycursor.execute(sql)

mydb.commit()

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
                    return 1
                else:
                    print("Did not enter character correctly")
                    return 0
            print("Searching for rider...")
            boolRiderFound = 1
            while(boolRiderFound):
                query = mycursor.execute("SELECT rideID FROM rides WHERE status = 'pending'")
                q = mycursor.fetchall()
                if(len(q) != 0):
                    boolRiderFound = 0
                    rideID = int(q[0][0])
                    print("Found a ride from ")
                    printRide(rideID)
                    answer = input("Would you like to take this ride?(Y/n): ")
                    if(answer == "Y"):
                        mycursor.execute(f"UPDATE rides SET status = 'accepted', driverID = {userID} WHERE rideID = {rideID}")
                        mydb.commit()
                        #mycursor.execute(f"UPDATE rides SET status = 'accepted' WHERE rideID = {rideID}")
                        #mydb.commit()
                        query = mycursor.execute(f"SELECT * FROM rides WHERE rideID = {rideID}")
                        q = mycursor.fetchall()
                        print(q)
                    else:
                        changeRiderStatus(userID, 0)
                        mydb.commit()
                        return 1
        elif userType == 0:
            userInput = input(
                "Would you like to change your status to available? \n (\'Y\' for yes and \'N\' for no): ")
            if userInput == 'Y':
                changeUserStatus(userID)
                userInput2 = input(
                    "Would you like to request a ride? \n (\'Y\' for yes and \'N\' for no): ")
                if userInput2 == 'Y':
                    rideID = createRide(userID)
                    print("Searching for driver...")
                    checkRideStatus(rideID)
                    print("Ride started...")
                    print("Ride ended.")
                    rateDriver(rideID)
                elif userInput == 'N':
                    print("bye")
                    return 0
                else:
                    print("Invalid Input")
                    return 0
            elif userInput == 'N':
                return 0
            else:
                print("Invalid Input")




            return 1
        
        


if __name__ == "__main__":
    main()



mydb.close()
