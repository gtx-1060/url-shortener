# url-shortener
 
 
## Compatibility
Check your Python version by typing in
```shell script
python --version
```
If you get the following
```shell script
Python 3.>7.*
```
the app has been tested and confirmed to be supported.


## Installation
1. Install [Poetry package manager](https://python-poetry.org/) if you haven't.
2. Go to the project folder and type in the console
```shell script
poetry install
```
3. Then create *.env* file in the *app* package, copy these text there and change values to your own.
```
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=YOUR_B_HOST
DB_NAME=YOUR_DB_NAME
SECRET_KEY=YOUR_SECRET_KEY_FOR_JWT_GENERATION
```
3. Run following command in console to create database tables.
```shell script
poetry run create_tables
```
4. Then type it to launch server.
```shell script
poetry run server
```

## Features
- Link shortening
- Link stats (private and public)
- Possibility to register for private link statistics
- Deleting a link after the expiration of visits/time (in progress)
- Bots protection (in progress)

## Documentation
You can open interactive *Swagger UI* documentaion in <your-hostname>/docs
```
http://<your-hostname>/docs
```
by default
 ```
http://127.0.0.1:8000/docs
```
 
