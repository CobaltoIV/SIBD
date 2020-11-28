#!/usr/bin/python3
import psycopg2

import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Transformers</title>')
print('</head>')
print('<body>')
print('<h3>Transformers</h3>')

print('<h1><a href="index.html"> Back to Index</a></h1>')
connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()

    print('<h4>Add Transformer</h4>')
    print('<form action = "insertransformer.cgi" method="post">')
    print('<p>pv :<input type = "number" name="pv"/></p>')
    print('<p>sv :<input type = "number" name="sv"/></p>')

    print('<p>Latitude, Longitude :<select name="gpscoord"/>')
    sql = """
        select gpslat,gpslong
        from substation
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(
            '<option value ="{},{}">{},{}</option>'.format(row[0],row[1],row[0],row[1]))
    print('</select></p>')

    print('<p>ID :<select name="id"/>')
    sql = """
        select id
        from element
        where id not in (select id from transformer t)
        and id not in (select id from line l)
        and id not in (select id from busbar);
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(
            '<option value={}>{}</option>'.format(row[0],row[0]))
    print('</select></p>')

    print('<p>Primary Busbar ID :<select name="bb1id"/>')
    sql = """
        select id
        from busbar
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(
            '<option value ={}>{}</option>'.format(row[0],row[0]))
    print('</select></p>')

    print('<p>Secondary Busbar :<select name="bb2id"/>')
    sql = """
        select id
        from busbar
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(
            '<option value ={}>{}</option>'.format(row[0],row[0]))
    print('</select></p>')
    print('<p><input type = "submit" name="Submit"/></p>')
    print('</form>')
    # Making query

    sql = 'SELECT * FROM transformer;'
    cursor.execute(sql)
    result = cursor.fetchall()
    num = len(result)
    # Displaying results
    # print('<p>{}</p>'.format(cursor.description(name)))
    print('<table border="0" cellspacing="5">')
    for row in result:
        print('<tr>')
        for value in row:
            # The string has the {}, the variables inside format() will replace the {}
            print('<td>{}</td>'.format(value))
        print(
            '<td><a href="removetransformer.cgi?id={}">Delete</a></td>'.format(row[0]))
        print('</tr>')
    print('</table>')
    # Closing connection
    cursor.close()

except Exception as e:
    # Print errors on the webpage if they occur
    print('<h1>An error occurred.</h1>')
    print('<p>{}</p>'.format(e))
finally:
    if connection is not None:
        connection.close()

    print('</body>')
    print('</html>')
