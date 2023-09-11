# Data-Engineer-Take-Home-Assignment

### How to Run the Container
1. Start up your container for the ETL process to run.
```bash
docker pull postgres
docker pull dpage/pgadmin4
docker volume create etl_job_positions
docker network create job_positions_network 
docker-compose up -d
```
2. Login to the DB Client pgadmin to query the tables


### Positions Database Design of Tables and Data Models

**Title table:** 
This is the parent table of Location table and the Remuneration table. It the main table that holds the basic information about each job position.

| Column name | Data type | Description |
|---|---|---|
| PositionID | integer | Primary key of the table |
| position_title | string | The title of the position |
| PositionURI | string | The URI of the position |

**Location table:** 
The Location table is a child table of the Title table and it stores the location information for each position.

| Column name | Data type | Description |
|---|---|---|
| PositionID | integer | Foreign key to Position table |
| LocationName | string | The name of the location |
| CountryCode | string | The country code of the location |
| CountrySubDivisionCode | string | The country subdivision code of the location |
| CityName | string | The city name of the location |
| Longitude | float | The longitude of the location |
| Latitude | float | The latitude of the location |

**Remuneration table:** 
The Remuneration table is also a child table of the Title table and it stores the remuneration information for each position.

| Column name | Data type | Description |
|---|---|---|
| PositionID | integer | Foreign key to Position table |
| MinimumRange | float | The minimum salary range for the position |
| MaximumRange | float | The maximum salary range for the position |
| RateIntervalCode | string | The rate interval code for the salary range |
| Description | string | The description of the salary range |


### DBML for the Tables Relationships
```sql
Table Position {
    position_id          varchar(50)   [primary key]
    position_title       varchar(100)  [not null]
    position_uri         varchar(200)  [unique]
    timestamp            timestamp     [not null]
}

Table PositionLocation {
    location_name            varchar(100)  [not null]
    country_code             char(15)       [not null]
    country_subdivision_code  varchar(50)   [not null]
    city_name                varchar(100)  [not null]
    longitude               float         [not null]
    latitude                float         [not null]

    // References
    position_id          varchar(50)  [ref: > Position.position_id]
}

Table PositionRemuneration {
    minimum_range            varchar(10)   [not null]
    maximum_range            varchar(10)   [not null]
    rate_interval_code        varchar(5)    [not null]
    description             varchar(20)   [not null]

    // References
    position_id          varchar(50)  [ref: > Position.position_id]
}
```
![DBML Diagram](/images/dbml.jpg "DBML Diagram")



### Describe which cloud services you would use to implement this in a cloud provider of your choosing. What are some pros and cons of your technology choice? 
1. **Event-Driven Architecture With AWS Lambda**:
Lambda builds a lean infrastructure on demand, scales continuously, and has a generous monthly free tier. Its execution time is capped at 15 minutes. If you have a task running longer than 15 minutes, you need to split it into subtasks and run them in parallel.
![DBML Diagram](/images/lambda.jpg "DBML Diagram")

2. **Event-Driven Architecture With Batch**: Batch environment and resources configuration is free-of-charge
but you only pay for compute resources consumed during task execution. Batch relies on AWS ECS to manage 
resources at the execution time by containerizing the solution, deploying the container and providing a predefined cluster environment to execute jobs
![DBML Diagram](/images/ecs.jpg "DBML Diagram")
