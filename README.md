# About fsnd_capstone

This is a project for Udacity fullstack nano degree.

Scenario: The Casting Agency models a company that is responsible for creating movies and managing and assigning actors
to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline
your process.

# Project dependencies

This project uses the following libraries

```
Flask==1.0.3
Flask-Migrate==2.7.0
Flask-Script==2.0.6
Flask-SQLAlchemy==2.4.0
gunicorn==20.1.0
psycopg2-binary==2.9.1
python-dotenv==0.19.0
python-jose-cryptodome==1.3.2
```

# Instructions for local development

1. git clone this repo.
2. Run command `pip install -r requirements.txt` from `fsnd_capstone` directory to install dependencies.
3. Create a local db by running `createdb castingcouch`.
4. Create tables by running `python manage.py db upgrade` from `fsnd_capstone` directory.
5. Run `flask run` from `fsnd_capstone` to run the server locally.

# Instructions to run unit tests locally

1. Create a test db locally via `createdb castingcouch_test`.
2. Create a file `secret.sh` in repo root directory.
3. Enter environment variables into `secret.sh`.
4. Run command `. ./secret.sh` from repo root directory.
5. Run command `dropdb castingcouch_test && createdb castingcouch_test && python test_casting_couch.py` to test.

# Instructions to deploy to Heroku

This app is hosted on https://fsnd-capstone-weizhi.herokuapp.com/

1. Deploy to Heroku by running `git push heroku master`

# Role-based access control

This app uses RBAC for its endpoint. The roles and permissions are as follows:

```
Casting Assistant: get:actors, get:movies
Casting Director: get:actors, get:movies, delete:actors, patch:actors, patch:movies, post:actors
Executive Producer: get:actors, get:movies, delete:actors, patch:actors, patch:movies, post:actors, post:movies, delete:movies
```

# API

### GET `/actors`

Fetches a paginated list of actors. Requires permission `get:actors`.

#### Parameters

Name | Type | In | Description
---|---|---|---
page | integer | query | which page number to request

#### Response

```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Bob",
      "age": "22",
      "gender": "M"
    },
    {
      "id": 2,
      "name": "Charlie",
      "age": "23",
      "gender": "M"
    },
    ...
  ]
}
```

### DELETE `/actors/{actor_id}`

Delete actor by id. Requires permission `delete:actors`.

#### Parameters

Name | Type | In | Description
---|---|---|---
actor_id | integer | path |

#### Response

```json
{
  "success": true,
  "deleted_id": 1
}
```

### POST `/actors`

Add new actor. Requires permission `post:actors`.

#### Parameters

Name | Type | In | Description
---|---|---|---
name | string | body | actor's name
age | integer | body | actor's age
gender | string | body | actor's gender

#### Response

```json
{
  "success": true,
  "actor": {
    "id": 2,
    "name": "Charlie",
    "age": "23",
    "gender": "M"
  }
}
```

### PATCH `/actors/{actor_id}`

Modify existing actor's information. Requires permission `patch:actors`.

#### Parameters

Name | Type | In | Description
---|---|---|---
actor_id | integer | path |
name | string | body | actor's name
age | integer | body | actor's age
gender | string | body | actor's gender

#### Response

```json
{
  "success": true,
  "actor": {
    "id": 2,
    "name": "Charlie",
    "age": "23",
    "gender": "M"
  }
}
```

### GET `/movies`

Fetches a paginated list of movies. Requires permission `get:movies`.

#### Parameters

Name | Type | In | Description
---|---|---|---
page | integer | query | which page number to request

#### Response

```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "title": "Avengers",
      "release_date": "Tue, 17 Aug 2021 12:53:07 GMT"
    },
    {
      "id": 2,
      "title": "Hobbit",
      "release_date": "Tue, 17 Aug 2021 12:53:07 GMT"
    },
    ...
  ]
}
```

### DELETE `/movies/{movie_id}`

Delete movie by id. Requires permission `delete:movie`.

#### Parameters

Name | Type | In | Description
---|---|---|---
movie_id | integer | path |

#### Response

```json
{
  "success": true,
  "deleted_id": 1
}
```

### POST `/movies`

Add new movie. Requires permission `post:movies`.

#### Parameters

Name | Type | In | Description
---|---|---|---
title | string | body | movie's title
release_date | string | body | movie's release date

#### Response

```json
{
  "success": true,
  "actor": {
    "id": 2,
    "title": "Hobbit",
    "release_date": "Tue, 17 Aug 2021 12:53:07 GMT"
  }
}
```

### PATCH `/movies/{movie_id}`

Modify existing movies's information. Requires permission `patch:movies`.

#### Parameters

Name | Type | In | Description
---|---|---|---
title | string | body | movie's title
release_date | string | body | movie's release date

#### Response

```json
{
  "success": true,
  "actor": {
    "id": 2,
    "title": "Hobbit",
    "release_date": "Tue, 17 Aug 2021 12:53:07 GMT"
  }
}
```