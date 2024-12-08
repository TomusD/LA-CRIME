# LA-CRIME Database Management System

  

  

This project is part of the M149: Database Management Systems course at the University of Athens. It involves designing, implementing, and demonstrating a database solution to manage crime data published by the Los Angeles Police Department (LAPD).

  

  

## Overview

  

  

The project focuses on:

  

- Normalizing and storing LAPD crime reports in a PostgreSQL database.

- Executing efficient queries to analyze and aggregate crime data.

- Developing a web application to provide user-friendly access to the database.

  

  

## Features

  
  

1.  **Database Design**

  

    - Normalized schema to store LAPD crime data efficiently.

    - Support for 27 fields from the dataset, ensuring no data loss.

  

  

2.  **Query Functionality**

  

    - Execute 13 complex SQL queries including:

        - Crime statistics by time, location, and type.

        - Co-occurrence of crimes and weapon usage.

        - Patterns in geographic and temporal data.

    - Efficient query execution using appropriate indexing.

  

3.  **Web Application**

  

    - User registration and authentication.

    - Query execution via web forms.

    - Crime data entry for authorized users.

  
  

## Technologies Used

  

-  **Database:** PostgreSQL

-  **Backend Framework:** Django

-  **Frontend Framework:** React

  
  

## Dataset

  

The dataset is sourced from the LAPD's publicly available records: [LAPD Crime Data (2020-Present)](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8).

  
  
  

## Queries Implemented

  

- Total requests per crime code within a time range.

- Most common crimes per area on a specific day.

- Average crimes per hour for a date range.

- Crime trends in specific geographic boundaries.

- And more.

  

## Usage Instructions

  

  

### 1. Clone the Repository

  

```bash
git  clone  https://github.com/TomusD/la-crime-database.git
cd  la-crime-database
```

  

  

### 2. Set Up the Environment

  

Install PostgreSQL and set up the database.

Create a virtual environment and install dependencies:

  

```bash
python  -m  venv  venv
source  venv/bin/activate
pip  install  -r  requirements.txt
```

  

To connect to your database, create an env file with the properties of the database, like this:

```
ENGINE=django.db.backends.postgresql
NAME=LA-CRIME
USER=<username>
PASSWORD=<password>
HOST=<host> # e.g., localhost
PORT=<port> # e.g., 5432
```

  

  

### 3. Load the Dataset

  

Load the LAPD dataset into the PostgreSQL database using the provided scripts.

  

```bash
py  manage.py  import_data
```

  

### 4. Run the Application

  

```bash
python  manage.py  runserver
```

  

### 5. Access the Application

  

```bash
Visit  http://<host>:<port>  in  your  browser.
(Note: The default port is 8000 unless specified otherwise.)
```

  

  

## License

  

This project is licensed under the MIT License.