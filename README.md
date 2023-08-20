# Hammer Systems Test Task - Simple Referal System

## Features
- Authorization with phone number.
- Ability to use invite code.

## How to run server locally

- Clone repo

```git clone https://github.com/AlexanderUp/simple_referal_system.git```

- Change directory

```cd simple_referal_system```

- Create virtual environment

```python3 -m venv venv```

- Activate virtual environment

```source venv/bin/activate```

- Install dependencies (no development dependencies like flake8, etc.)

```python3 -m pip install -r requirements/base.txt```

- Install dependencies (with development dependencies like flake8, etc.)

```python3 -m pip install -r requirements/dev.txt```

- Install dependencies (with test dependencies like pytest, etc.)

```python3 -m pip install -r requirements/test.txt```

- Create .env file in referal_system (where .env.example is) and set django secret key

- Apply migrations

```python3 manage.py migrate```

- Create superuser

```python3 manage.py createsuperuser```

- Run server

```python3 manage.py runserver```

- API description is available with Swagger or Redoc at

```http://127.0.0.1:8000/swagger/```

```http://127.0.0.1:8000/redoc/```


### System description

- Send your phone number and get authorization code (2 seconds delay emulated) with

```POST http://127.0.0.1:8000/api/v1/authorize/```

- Send give authorization code and get token to

```POST http://127.0.0.1:8000/api/v1/login/```

- Your profile is available at (given token for authorization required)
(authentication header AUTHORIZATION is 'Token token_string')

```GET http://127.0.0.1:8000/api/v1/users/me/```

- You can use invitation code (only once and not your own) at

```POST http://127.0.0.1:8000/api/v1/users/invite/```

### Hosting

Project deployed and available at
```https://alexanderup.pythonanywhere.com/```


### Author comments

Used DB is sqlite3 because pythonanywhere doesn't allow to serve Postgres DB instance for free accounts.
