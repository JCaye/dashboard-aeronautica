# dashboard-aeronautica
## What is this?
This is an application built to aggregate and display relevant information on aeronautical incidents and accidents.

## How to use it?
This application is hosted live [here](https://dashboard-aviacao-heroku.herokuapp.com/board/).
To run it in locally, clone the repo and install its dependencies inside a virtual environment. Run `set FLASK_APP=dashboard` followed by `flask run` and access the page at `localhost:5000/board`.

### Built with
* Python 3.7
* [Flask](http://flask.pocoo.org/) - web framework
* [SQLAlchemy](https://www.sqlalchemy.org/) - database library for python
* [ChartJS](http://www.chartjs.org/) - JavaScript library for plotting pretty charts

## Files breakdown
* `dashboard/__init__.py` - instantiates the app and registers the `board` [blueprint](http://flask.pocoo.org/docs/1.0/blueprints/) to it
* `dashboard/board.py` - provides mapping for the endpoints and passes the information to be displayed
* `dashboard/db.py` - provides SQLAlchemy engines and sessions for interacting with the database
* `dashboard/model.py` - defines the entities and relationships mapped in the database
* `dashboard/service.py` - queries and processes database information, delivering it to `board.py`
* `dashboard/registro.db` - sqlite database
* `dashboard/templates/board.html` - html of the page to display