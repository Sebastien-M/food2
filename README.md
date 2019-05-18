
# Food2 
  
A Django web app allowing you to choose a recipe to cook for each day of the week.
Once your recipe chosen, all its required ingredients will be added to a shopping list that you can modify
  
## Getting Started  
  
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.  
  
### Prerequisites  
  
To run the project you will need
    - Python (at least 3.5)
    - MySQL or MariaDB
    - (optional) [pipenv](https://docs.pipenv.org/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/) modules to manage your Python virtualenvs
  
### Installing  
  
A step by step series of examples that tell you how to get a development env running  
  
Clone the repo:
`git clone https://github.com/Sebastien-M/food2.git`  
  
Install requirements:
`pip install -r Pipfile`  
or if you are using pipenv
`pipenv install`

Create your database in MySQL/MariaDB:
`CREATE DATABASE <db_name>;`

Inside food2/deploy create a file called 'secrets_local.py' and fill the values:
```
import os  
  
SECRETS_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
SECRETS_ALLOWED_HOSTS 	= <span style="color:red">['*']  
SECRETS_DB_NAME 		= <span style="color:red">'your db name'</span>
SECRETS_DB_USER 		= <span style="color:red">'your db user'</span>  
SECRETS_DB_PASS 		= <span style="color:red">'your db pass'</span>  
SECRETS_DB_HOST 		= <span style="color:red">'your db host'</span>
SECRETS_DB_PORT 		= <span style="color:red">'your db port'</span>
SECRETS_DEBUG 			= <span style="color:red">True or False</span>
SECRETS_STATIC_URL 		= <span style="color:red">'/static/'</span>  
SECRETS_STATIC_ROOT 	= <span style="color:red">os.path.join(SECRETS_BASE_DIR, '/static/') </span> 
SECRETS_LOG_PATH 		= <span style="color:red">'./debug.log'</span> 
SECRETS_SECRET_KEY 		= <span style="color:red">'your secret key'</span>
```

Start your virtualenv if you are using one
If you are using pipenv:
`pipenv shell` 
at the root of the repository

Run Django migrations:
`python manage.py food2/manage.py migrate`

Create a user to have access to the admin site:
`python manage.py createsuperuser`

Run the developpement server:
`python manage.py runserver`

The project also comes with a custom command to populate the database with recipes and their ingredients:
`python manage.py fill database <ingredient_name>`
You can pass multiple ingredients names separated with a space.
This command will scrap [marmiton](https://marmiton.org) website and search for recipes with specified ingredients

## Running the tests

TODO


## Deployment

  Gunicorn is used to run the application in production environment, you can read the doc [here](https://gunicorn.org/#deployment)) to see how to deploy it.
  Gunicorn is present in the Pipfile you previously installed and should be available.

## Versioning

I use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Sebastien-M/food2/releases).

## Authors

* **Sébastien Mandaba** - *Initial work* - [github](https://github.com/Sebastien-M)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* Potato
