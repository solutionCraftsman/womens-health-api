## Women's Health API!

### Installation Guide
To skip installing locally, the API service is hosted [here](https://awtwvo.herokuapp.com).

* Clone this Repository
* Preferably, set up a virtual environment. You can follow the guide [here](https://docs.python.org/3/library/venv.html).
* While in the root directory, run "pip install requirements.txt" to install the required packages.
* Start the server by running "python manage.py runserver"

### API Documentation

#### Requests
Predict the predicted dates of a lady’s estimated period cycles within a timeframe.
```http
POST /womens-health/api/create-cycles
```

