#!/usr/bin/env python
import time, sys
if sys.platform == "linux2":
	import MySQLdb
elif sys.platform == "darwin":
	import mysql.connector

class MySQLConnection:

	def __init__(self, id = None):
		self.hostName 	= "localhost"
		self.userID 	= "root"
		self.password	= "verateam"
		self.dataBase	= "Vera"
		self.logging = False

	def getID(self):
		return self.id


	def stopLogging(self):
		self.logging = False

	def startLogging(self):
		if not self.logging:
			self.logging = True
			#Insert ID and timestamp in ECULogs table
			self.runSQLCommand("INSERT INTO ECULogs () values ();")
			self.id = self.cursor.lastrowid
			print("Session ID: " + str(self.id));

			#Create table for this session
			createDBquery = """
							CREATE TABLE IF NOT EXISTS ECULog%s
							(`id` int(11) NOT NULL AUTO_INCREMENT,
							`lat_loc` varchar(15) COLLATE utf8_swedish_ci NOT NULL,
							`long_loc` varchar(15) COLLATE utf8_swedish_ci NOT NULL,
							`speed` varchar(15) NOT NULL,
							`timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
							`rpm` varchar(20) NOT NULL,
							`tempcylinder` varchar(20)  NOT NULL,
							`temptoplock` varchar(20)  NOT NULL,
							`tempmotorblock` varchar(20)  NOT NULL,
							`batterispanning` varchar(20)  NOT NULL,
							`lufttryck` varchar(20)  NOT NULL,
							`lufttemp` varchar(20)  NOT NULL,
							`branslemassa` varchar(20)  NOT NULL,
							`error_code` varchar(20)  NOT NULL,
							PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci AUTO_INCREMENT=1;
							""" % str(self.id)	
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
			self.conn.close()
				

	def saveHMILog(self, date, level, module, message, gpsPos):
		message = "INSERT INTO HMILog (day,level,module,msg,lat_loc,long_loc) VALUES (\'" + date + "','" + str(level) + "','" + str(module) + "','" +  message  + "','" + str(gpsPos[0])  + "','" + str(gpsPos[1]) + "')"
		#print(message)
		self.runSQLCommand(message)


	def saveLog(self, logValues):
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
			query = "INSERT INTO ECULog" + str(self.id) + " (tempcylinder, temptoplock, tempmotorblock, batterispanning , lufttryck, lufttemp, rpm, branslemassa, error_code, lat_loc, long_loc, speed) VALUES (" + values + ");" 
			self.runSQLCommand(query)


if __name__ == '__main__':
		conn = MySQLConnection()
		conn.runSQLCommand("SHOW TABLES")
		print(conn.cursor.fetchall())