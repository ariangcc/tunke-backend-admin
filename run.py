import sys
from app import create_app

app = None
if(sys.argv[1] == "db"):
    app_type = 0
else:
    app_type = int(sys.argv[1])
print(app_type)
if app_type == 0:
    app = create_app('configclient', app_type)
else:
    app = create_app('configadmin', app_type)

print(app.config['PORT'])

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])