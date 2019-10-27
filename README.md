# Cricket-Fantasy-League

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

For updating a SQL , checkout `config.py`. Once appropriate user is added, run
```bash
$ flask db upgrade
```

## Starting app

To start the app, run
```bash
$ python cfl.py
```

## Contributors
- Shanthanu S Rai
- Varun Pattar
