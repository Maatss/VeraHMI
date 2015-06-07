#!/usr/bin/env python

import sys, time

#Import different mysql modules depending on OS (MySQLdb doesn't work in OS X and mysql.connector doesn't work in linux...)
if sys.platform == "linux2":
	import MySQLdb
elif sys.platform == "darwin":
	import mysql.connector

class LogMySQL:

	def __init__(self, logNames, MySQLCreationString):
		self.hostName 	= "localhost"
		self.userID 	= "root"
		self.password	= "verateam"
		self.dataBase	= "Vera"
		self.logging = False
		self.loggNames = logNames
		self.MySQLCreationString = MySQLCreationString



#######################################################################################
################################## Class functions ####################################
#######################################################################################

	def getID(self):
		return self.id

	def stopLogging(self):
		self.logging = False

	def startLogging(self):
		if not self.logging:
			self.logging = True
			#Insert ID and timestamp in ECULogs table
			self.runSQLCommand("INSERT INTO HSLogs () values ();")
			self.id = self.cursor.lastrowid
			print("Database session started, ID: " + str(self.id));

			#Create table for this session
			createDBquery = self.MySQLCreationString % str(self.id)	
			self.runSQLCommand(createDBquery)


	def runSQLCommand(self, sql_string):
		try:
			if sys.platform == "linux2":
				self.conn = MySQLdb.connect(user=self.userID, 
											passwd=self.password, 
											host=self.hostName, 
											db=self.dataBase)
			else:
				self.conn = mysql.connector.connect(user=self.userID, 
													password=self.password, 
													host=self.hostName, 
													database=self.dataBase)

			self.cursor = self.conn.cursor()
			self.cursor.execute(sql_string)
			self.conn.commit()
			self.conn.close()

		except Exception as e:
			print("Error in MySQLConnection: " + str(e))
			if self.conn.open:
				self.conn.close()
			


	def saveLog(self, logValues):
		#Only log values if timer is running (self.logging == True)
		if self.logging:
			values = ""
			for x in range(len(logValues)):
				if(x==0):
					values += "'" + str(logValues[x]) + "','"
				elif(x != len(logValues)-1):
					values += str(logValues[x]) + "','"
				else:
					values += str(logValues[x]) + "'"
			#print(values)
			self.logNamesString = ""
			for i in range(len(self.logNames)):
				self.logNamesString += str(self.logNames + ",")
			self.logNamesString = self.logNamesString[:-1]

			query = "INSERT INTO HSLog" + str(self.id) + " ("  + self.logNamesString + ") VALUES (" + values + ");" 
			self.runSQLCommand(query)
			



