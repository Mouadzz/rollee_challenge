# Rollee Task - Backend Engineer Coverage Team



## Description

This project is a Python program that performs the login on the Rollee dashboard (https://dashboard.getrollee.com/) using provided credentials and extracts all the accounts for a given user ID. The program fetches the required account information and returns a tidy and structured JSON response. It handles all possible errors, such as invalid credentials and unexpected responses.

## Getting Started

To get started with the project, follow these steps:

```bash
git clone https://github.com/Mouadzz/rollee_challenge.git

cd rollee_challenge

docker compose up
```

## API Endpoints

POST `/dashboard/login_and_get_accounts`

Login to rollee dashboard using provided credetials and extracts all the accounts for a given user ID.

Accepts a JSON request containing the username, password, and user_id, and returns a JSON response with the extracted account details.

Example Request:
```
import requests
import json

url = "http://127.0.0.1:8000/dashboard/login_and_get_accounts"

payload = json.dumps({
  "username": "test_candidate",
  "password": "test_candidate123",
  "user_id": "de344889-428a-4be0-93d4-d286d02a7252"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
```
Example Response:
```
{
    "accounts": [
        {
            "account_id": "ac70a627-561a-4fa9-a86b-c8a8f7d73c2e",
            "name": "Anne Herrmann",
            "email": "AnneHerrmann@teleworm.us",
            "platform_name": "Bolt",
            "country": "ar",
            "currency": "",
            "gross_earnings": 0.0
        },
        {
            "account_id": "ea8eab61-84cf-438c-a385-8f93a693c087",
            "name": "Taylor Lloyd",
            "email": "TaylorLloyd@teleworm.us",
            "platform_name": "Deel",
            "country": "ar",
            "currency": "",
            "gross_earnings": 0.0
        }
    ]
}
```

## How to run unit tests
```
docker-compose exec rollee python manage.py test
```

