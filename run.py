import sys
from app import CreateApp
from time import sleep
from flask import Flask, render_template
import logging

app = None
if(sys.argv[1] == "db"):
	appType = 0
else:
	appType = int(sys.argv[1])
print(appType)
if appType == 0:
	app = CreateApp('configclient', appType)
	logging.basicConfig(filename='errorClient.txt', level=logging.DEBUG)
else:
	app = CreateApp('configadmin', appType)
	logging.basicConfig(filename='errorAdmin.txt', level=logging.DEBUG)

print(app.config['PORT'])

if __name__ == '__main__':
	app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])