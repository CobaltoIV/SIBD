#!/usr/bin/python3
import psycopg2, cgi
import login

#print('Location: ./busbar.cgi')
#print()
form = cgi.FieldStorage()
#getvalue uses the names from the form in previous page
id = form.getvalue('id')
print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Project</title>')
print('</head>')
print('<body>')
print('<h1><a href="../index.html"> Back to Index</a></h1>')
print('<h2><a href="transformers.cgi"> Back to Transformers</a></h2>')
connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    # Making query
    sql = 'DELETE FROM transformer WHERE id = %s;' 
    # The string has the {}, the variables inside format() will replace the {}
    #print('<p>{}</p>'.format(sql % id))
    # Feed the data to the SQL query as follows to avoid SQL injection
    cursor.execute(sql , [id])
    # Commit the update (without this step the database will not change)
    sql = 'DELETE FROM element WHERE id = %s;' 
    # The string has the {}, the variables inside format() will replace the {}
    #print('<p>{}</p>'.format(sql % id))
    # Feed the data to the SQL query as follows to avoid SQL injection
    cursor.execute(sql , [id])
    # Commit the update (without this step the database will not change)
    connection.commit()
    # Closing connection
    cursor.close()
    print('<p> SUCCESS</p>')
except Exception as e:
    # Print errors on the webpage if they occur
    print('<h1>An error occurred.</h1>')
    #print('<p>{}</p>'.format(e))
finally:
    if connection is not None:
        connection.close()
print('</body')
print('</html>')