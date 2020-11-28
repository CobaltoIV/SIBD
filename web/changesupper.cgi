#!/usr/bin/python3
import cgi

form = cgi.FieldStorage()

name = form.getvalue('sname')
address = form.getvalue('saddress')
lati = form.getvalue('gpslat')
longi = form.getvalue('gpslong')
locality = form.getvalue('locality')

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Lab 09</title>')
print('</head>')
print('<body>')

# The string has the {}, the variables inside format() will replace the {}
print('<h3>Change supervisor for substation {} {} in {} ......{},{}</h3>'.format(lati,longi,locality,name,address))

# The form will send the info needed for the SQL query
print('<form action="updatesupervisor.cgi" method="post">')
print('<p><input type="hidden" name="gpslat" value="{}"/></p>'.format(lati))
print('<p><input type="hidden" name="gpslong" value="{}"/></p>'.format(longi))
print('<p>New Name: <input type="text" name="sname"/></p>')
print('<p>New address: <input type="text" name="saddress"/></p>')
print('<p><input type="submit" value="Submit"/></p>')
print('</form>')

print('</body>')
print('</html>')