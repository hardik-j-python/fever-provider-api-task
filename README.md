# Fever Providers API

### Technology Used
 
- Python 3.10.9
- Django
- Rest API
- Django Rest Framework
- PostgreSQL
- Swagger (for API documentation)

### Before executing below commands, check the attached "env-sample" at src/config/.env -sample and change the details

### Steps to setup the project (To execute the below commands, your path would be src/ directory)

* First time
```
make first-time
```

* To update the dependencies of the project (i.e. packages)
```
make install-dependencies
```

* Migrate the changes to the database
```
make migrate
```

* Fetch the data provider and store those in the database
```
make load-data
```

* To run the server in your machine
```
make run
```

### The API is developed as per the requrement, please check below information
#### API URL: ```https://localhost:PORT/api/events/search/``` (it takes the 2 query parameters starts_at and ends_at)
#### Swagger documentation: ```https://localhost:PORT/swagger/```