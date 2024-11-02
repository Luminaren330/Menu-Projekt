# Getting Started with Flask API.

Python supported version: 3.11

## Create venv

In the project directory, you can run:

### `python -m venv venv`

Activate venv using:

### `venv/Scripts/activate`

Move to the backend directory:

### `cd .\Backend\`

## Install required libraries

### `pip install -r requirements.txt`

## Create environmental variables

In modules directory create `.env` file. Define secret key and database credentials inside this file.

Example file content:

```
SECRET_KEY=xyz #you can type anything
DB_USER=postgres
DB_PASSWORD=your_password
DB_URL=localhost
DB_DBNAME=your_db_name
```

## Run Flask server

### `python app.py`

Open [http://localhost:5000](http://localhost:5000) to view it in your browser.