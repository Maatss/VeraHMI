#!/usr/bin/env python
import time, sys

class MySQLConnection:

	def __init__(self, parent=None, **options):
		self.hostName 	= "localhost"
		self.userID 	= "root"
		self.password	= "verateam"
		self.dataBase	= "Vera"
			
		if sys.platform == "linux2":
			import MySQLdb
		else:
			import mysql.connector

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
						`timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
						`rpm` varchar(20) NOT NULL,
						`tempcylinder` varchar(20)  NOT NULL,
						`temptoplock` varchar(20)  NOT NULL,
						`tempmotorblock` varchar(20)  NOT NULL,
						`batterispanning` varchar(20)  NOT NULL,
						`lufttryck` varchar(20)  NOT NULL,
						`lufttemp` varchar(20)  NOT NULL,
						`branslemassa` varchar(20)  NOT NULL,
						`tandpos` varchar(20)  NOT NULL,
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

		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your user name or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		

	def saveLog(self, logValues):
		values = ""
		for x in range(len(logValues)):
			if(x==0):
				values += "'" + str(logValues[x]) + "','"
			elif(x != len(logValues)-1):
				values += str(logValues[x]) + "','"
			else:
				values += str(logValues[x]) + "'"
		query = "INSERT INTO ECULog" + str(self.id) + " (tempcylinder, temptoplock, tempmotorblock, batterispanning , lufttryck, lufttemp, rpm, branslemassa, tandpos, lat_loc, long_loc) VALUES (" + values +  ");" 
		self.runSQLCommand(query)


if __name__ == '__main__':
		conn = MySQLConnection()
		conn.runSQLCommand("SHOW TABLES")
		print(conn.cursor.fetchall())