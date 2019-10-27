# Cricket-Fantasy-League

All live cricket updates are obtained from [https://www.espncricinfo.com](https://www.espncricinfo.com/).

## Setup

`requirements.txt` contains all the required packages. Preferably use a virtual environment. Run 
```bash
$ pip install -r requirements.txt
```

MySQL is used for the database. The database name is assumed to be  `cfl`.

SQLAlchemy will require the following
```bash
$ sudo apt-get install libmysqlclient-dev
```

For setting up the database, checkout `config.py`. Once appropriate database is created, run
```bash
$ flask db upgrade
```

All latest cricket player details can be obtained by running python scripts in `scripts` folder. Place the CSV files generated in
csv folder and run `add_records_to_db.py` to add latest player details to database.

## Starting app

To start the app, run
```bash
$ python cfl.py
```

## Contributors
- Shanthanu S Rai
- Varun Pattar
