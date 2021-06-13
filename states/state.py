#!/usr/bin/python3
import cgi

def get_cmd():
  args = cgi.FieldStorage()
  cmd = args['cmd'].value
  return cmd

cmd = get_cmd()
state = " ".join(cmd.split('_'))
print("Content-Type: text/html\n")
print(f"<html> <head> <center><h1>{state} Covid-19 Data</h1></center> </head>")
print("<body>")

print(f'<img src="make_fig.py?cmd={cmd}">')

print("</body></html>")
