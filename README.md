
# Food2 
  
A Django web app allowing you to choose a recipe to cook for each day of the week.
Once your recipe chosen, all its required ingredients will be added to a shopping list that you can modify
  
## Getting Started  
  
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.  
  
### Prerequisites  
  
To run the project you will need:
* Python (at least 3.5)
* MySQL or MariaDB
* (optional) [pipenv](https://docs.pipenv.org/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/) modules to manage your Python virtualenvs
  
### Installing  
  
A step by step series of examples that tell you how to get a development env running  
  
Clone the repo:
```
git clone https://github.com/Sebastien-M/food2.git
```  
  
Install requirements:
```
pip install -r Pipfile
```  
or if you are using pipenv
```
pipenv install
```

Create your database in MySQL/MariaDB:
```
CREATE DATABASE <db_name>;
```

Inside food2/deploy create a file called 'secrets_local.py' and fill the values:
```python
import os  
  
SECRETS_BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_ALLOWED_HOSTS   = ['*']
SECRETS_DB_NAME         = 'your db name'
SECRETS_DB_USER         = 'your db user'
SECRETS_DB_PASS         = 'your db pass'
SECRETS_DB_HOST         = 'your db host'
SECRETS_DB_PORT         = 'your db port'
SECRETS_DEBUG           = True
SECRETS_STATIC_URL      = '/static/'
SECRETS_STATIC_ROOT     = os.path.join(SECRETS_BASE_DIR, '/static/')
SECRETS_LOG_PATH        = './debug.log'
SECRETS_SECRET_KEY      = 'your secret key'
```

Start your virtualenv if you are using one
If you are using pipenv:
```
pipenv shell
``` 
at the root of the repository

Run Django migrations:
```
python manage.py food2/manage.py migrate
```

Create a user to have access to the admin site:
```
python manage.py createsuperuser
```

Run the developpement server:
```
python manage.py runserver
```

The project also comes with a custom command to populate the database with recipes and their ingredients:
```
python manage.py fill database <ingredient_name>
```
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Potato
