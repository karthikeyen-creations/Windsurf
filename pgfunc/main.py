from flask import Flask
from app.dao.database import engine
from app.templates import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/")
def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    app.run(debug=True)
