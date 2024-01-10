from blog import app, db

try:
	app.app_context().push()
	db.create_all()
	print("Database successfully created!")
except:
	print("There was a problem creating the database")
