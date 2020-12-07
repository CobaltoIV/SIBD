#!/usr/bin/python3
import psycopg2

import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Lab 09</title>')
print('</head>')
print('<body>')
print('<h1><a href="../index.html"> Back to Index</a></h1>')
print('<h2>Supervisor change</h2>')

connection = None
try:
	# Creating connection
	connection = psycopg2.connect(login.credentials)
	cursor = connection.cursor()

	print('<h3>Latitude | Longitude | Locality | Supervisor Name | Supervisor Address</h3>')
	# Making query
	sql = 'SELECT * FROM substation;'
	cursor.execute(sql)
	result = cursor.fetchall()
	num = len(result)

	# Displaying results
	print('<table border="0" cellspacing="5">')
	
	for row in result:
		print('<tr>')
		for value in row:
		# The string has the {}, the variables inside format() will replace the {}
			print('<td>{}</td>'.format(value))
		print('<td><a href="changesupper.cgi?gpslat={}&gpslong={}&locality={}&sname={}&saddress={}">Change Supervisor</a></td>'.format(row[0],row[1],row[2],row[3],row[4]))
		print('</tr>')
	print('</table>')

	# Closing connection
	cursor.close()
except Exception as e:
	# Print errors on the webpage if they occur
	print('<h1>An error occurred.</h1>')
	#print('<p>{}</p>'.format(e))
finally:
	if connection is not None:
		connection.close()

print('</body>')
print('</html>')