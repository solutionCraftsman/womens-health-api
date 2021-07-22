## Women's Health API!

### Installation Guide
To skip installing locally, the API service is hosted [here](https://womens-health-api.herokuapp.com/).

* Clone this Repository
* Preferably, set up a virtual environment. You can follow the guide [here](https://docs.python.org/3/library/venv.html).
* While in the root directory, run "pip install requirements.txt" to install the required packages.
* Start the server by running "python manage.py runserver"

### API Documentation

#### Request
Predict the dates of a lady’s estimated period cycles within a timeframe.
```http
POST /womens-health/api/create-cycles
```

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `last_period_date` | `string` | **Required**. Last date period started. | '2021-01-01' |
| `cycle_average` | `integer` | **Required**. Average number of days a cycle takes | 25 |
| `period_average` | `integer` | **Required**. Average number of days a period flow takes | 5 |
| `start_date` | `string` | **Required**. Date to begin creating cycle  | '2021-02-01' |
| `end_date` | `string` | **Required**. Date to begin creating cycle  | '2022-02-01' |

#### Responses

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** <br>
    ```javascript
    {
      "create_cycle_request_id" : integer,
      "total_created_cycles": integer
    }
    ```

    The `create_cycle_request_id` attribute is the id of the request that was made. This id maps to each of the period cycles created and has to be provided when a date is supplied to predict the event.
    
    The `total_created_cycles` attribute is the number of cycles created from the start date to the end date.
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** <br> 
    ```javascript
    {
      "message": "Error in request data"
    }
    ```

#### Request
Returns the event happening in a lady’s cycle for the specified day.
```http
GET /women-healths/api/cycle-event?create_cycle_request_id=<integer>&date=<string>
```

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `create_cycle_request_id` | `integer` | **Required**. ID of the initial request used to create the period cycles. | 1 |
| `date` | `string` | **Required**. Date for which event is to be returned  | '2021-01-01' |

#### Responses

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** <br>
    ```javascript
    [
       {
          "event":"fertility_window",
          "date":"2021-01-01”
       }
    ]
    ```
  
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** <br> 
    ```javascript
    {
      "message": "Request with id <id> not found"
    }
    ```

  * **Code:** 404 NOT FOUND <br />
    **Content:** <br> 
    ```javascript
    {
      "message": "No Event Found for date <date>"
    }
    ```

  * **Code:** 400 BAD REQUEST <br />
    **Content:** <br> 
    ```javascript
    {
      "message": "Error in request parameter"
    }
    ```

