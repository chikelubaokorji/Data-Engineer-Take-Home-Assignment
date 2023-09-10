import datetime
import requests
import psycopg2
from psycopg2 import sql
# from ratelimiter import RateLimiter


TIMEOUT = 5
MAX_ROWS_PER_QUERY = 500
API_KEY = "gh3jLR00nD4jPbv2Z4GUEwkWfGtyQvz96Kc3JeHTDa0="

query_params = { 
    "Keyword": "data engineering",
    "LocationName": "Chicago",
    "ResultsPerPage": MAX_ROWS_PER_QUERY 
}

db_params = {
    "database": "job_positions",
    "user": "postgres",
    "password": "123456",
    "host": "pgdatabase",
    "port": "5432"
}

# DATABASE="job_positions"
# HOST="pgdatabase"
# USER="postgres"
# PASSWORD="123456"
# PORT="5432"

position_query = "INSERT INTO \"Position\" (position_id, position_title, position_uri, timestamp) VALUES (%s,%s,%s,%s)"

location_query = "INSERT INTO \"PositionLocation\" (location_name, country_code, country_subdivision_code, city_name, longitude, latitude, position_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"

remuneration_query = "INSERT INTO \"PositionRemuneration\" (minimum_range, maximum_range, rate_interval_code, description,position_id) VALUES (%s,%s,%s,%s,%s)"

def create_tables(connection):
    cursor = connection.cursor()
    try:
        with open('../database/create_tables.sql', 'r', encoding='utf-8-sig') as file:
            sql_statements = file.read().split(';')
            for sql_statement in sql_statements:
                if sql_statement.strip():
                    cursor.execute(sql.SQL(sql_statement))
        connection.commit()
        print("Tables created successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Error: {str(e)}")
    finally:
        cursor.close()


def load_data(connection, data):
    queries = [position_query, location_query, remuneration_query]
    cursor = connection.cursor()
    try:
        for query, i in zip(queries, data):
            cursor.executemany(query, i)
            connection.commit()
        print("Tables loaded successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Error: {str(e)}")
    finally:
        cursor.close()


def get_jobs():
    # url = "https://data.usajobs.gov/api/Search?Keyword=data engineering&LocationName=Chicago"
    url = "https://data.usajobs.gov/api/Search"
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "your@email.address",
        "Authorization-Key": API_KEY
    }
    response = requests.get(url, params=query_params, headers=headers, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        return data["SearchResult"]["SearchResultItems"]
    else:
        raise Exception("Error fetching jobs: {}".format(response.status_code))

def process_data():
    position = []
    location = []
    remuneration = []

    position_keys = ["PositionID", "PositionTitle", "PositionURI"]
    location_keys = ["LocationName", "CountryCode", "CountrySubDivisionCode", "CityName", "Longitude", "Latitude"]
    remuneration_keys = ["MinimumRange", "MaximumRange", "RateIntervalCode", "Description"]
    
    jobs = get_jobs()
    for i in range(len(jobs)):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        position_id = jobs[i]["MatchedObjectDescriptor"]["PositionID"]

        position_tuple = tuple(jobs[i]["MatchedObjectDescriptor"][key] for key in position_keys)
        position.append(position_tuple + (timestamp,))

        location_tuple = tuple(jobs[i]["MatchedObjectDescriptor"]["PositionLocation"][0][key] for key in location_keys)
        location.append(location_tuple + (position_id,))

        remuneration_tuple = tuple(jobs[i]["MatchedObjectDescriptor"]["PositionRemuneration"][0][key] for key in remuneration_keys)
        remuneration.append(remuneration_tuple + (position_id,))
    return [position, location, remuneration]


if __name__ == "__main__":
    try:
        connection = psycopg2.connect(**db_params)
        create_tables(connection)
        data = process_data()
        load_data(connection, data)
    except Exception as e:
        print(f"Database connection error: {str(e)}")
    finally:
        connection.close()