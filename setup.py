from blog import app, db

try:
	with open(".env", "w") as file:
		file.write(f"SECRET_KEY=<Your made-up secret key for the application>")
	print(".env file successfully created!")
except Exception as e:
	print("There was a problem creating the .env file: {e}")

try:
	app.app_context().push()
	db.create_all()
	print("Database successfully created!")
except:
	print("There was a problem creating the database")
