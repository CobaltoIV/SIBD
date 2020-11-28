#!/usr/bin/python3
import psycopg2, cgi
import login
import string

form = cgi.FieldStorage()
#getvalue uses the names from the form in previous page
pv = form.getvalue('pv')
sv = form.getvalue('sv')
gps = form.getvalue('gpscoord')
words = gps.split(',')
lat = words[0]
long = words[1]
id  = form.getvalue('id')
bb1id  = form.getvalue('bb1id')
bb2id  = form.getvalue('bb2id')
print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Project</title>')
print('</head>')
print('<body>')

print('<h1><a href="index.html"> Back to Index</a></h1>')
print('<h2><a href="transformers.cgi"> Back to Transformers</a></h2>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    # Making query
    sql = 'INSERT INTO transformer VALUES(%s,%s,%s,%s,%s,%s,%s);' #(id,pv,sv,lat,long,bb1id,bb2id)
    data = (id,pv,sv,lat,long,bb1id,bb2id)
    # The string has the {}, the variables inside format() will replace the {}
    print('<p>{}</p>'.format(sql % data))
    # Feed the data to the SQL query as follows to avoid SQL injection
    cursor.execute(sql, data)
    # Commit the update (without this step the database will not change)
    connection.commit()
    # Closing connection
    cursor.close()
except Exception as e:
    # Print errors on the webpage if they occur
    print('<h1>An error occurred.</h1>')
    print('<p>{}</p>'.format(e))
finally:
    if connection is not None:
        connection.close()
print('</body')
print('</html>')
