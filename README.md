# About 

This repository was made for the "Data Modeling With Postgres" project by Udacity for their Data Engineer program.

------------------------
# Purpose 

In this project, we will be building a database in Postgres for the startup Sparkify.
Sparkifys has a new music streaming app that they wish to analyze their user activity via the data they have been collecting on their user's activities. 
However, Sparkify analytics team doesn't have an easy way to query their data because they all reside in a directory of JSON logs. 
Our goal is to create a database and insert Sparkify data logs into it so they can achieve their analytical objectives.

------------------------

# Database Schema Design

The database is designed in a star schema.
The benefits of star schemas are that they're optimized for reads speed, optimized aggregation speed, and allow for simplified queries with minimal amounts of joins.

## Table schema 

### Songplays table
 - songplay_id serial PRIMARY KEY
 - start_time timestamp
 - user_id int
 - level varchar
 - song_id varchar
 - artist_id varchar
 - session_id int
 - location varchar
 - user_agent varchar

### Users table
 - user_id int PRIMARY KEY
 - first_name varchar
 - last_name varchar
 - gender varchar
 - level varchar

### Songs table
- song_id varchar PRIMARY KEY
- title varchar
- artist_id varchar
- year int
- duration float8

### Artists table
- artist_id varchar PRIMARY KEY
- name varchar
- location varchar
- latitude float8
- longitude float8

### Time table
- start_time timestamp PRIMARY KEY
- hour int
- day int
- week int
- month int
- year int
- weekday int


------------------------

# Requirements
- Postgres server with:
	- User call "student with the password "student" and CREATEDB permission
	- Database named "studentdb"
- Python3 with the following packages:
	- Psycopg2
	- Pandas 

------------------------

# How to Run
The Postgres server should be up before running the project.

```
python create_tables.py
python etl.py
```
