from flask_migrate import MigrateCommand,Migrate
from flask_script import Manager
from App import create_app
from flask_bootstrap import Bootstrap
app=create_app()

manager=Manager(app)

bootstrap=Bootstrap(app=app)

manager.add_command('db', MigrateCommand)

if __name__=='__main__':

    manager.run(debug=True)
