import html
import re
import requests
from .exceptions import CustomException


def parse_html(regex, response):
    """
    Parse HTML content using a regular expression and return matching groups.
    """
    matches = re.search(
        regex, response.content.decode("utf-8"))
    return matches


def get_access_token(code, cookies):
    """
    Get the access token using the parsed code from the Location header 
    """

    body = {
        "grant_type": "authorization_code",
        "client_id": "dashboard",
        "redirect_uri": "https://dashboard.getrollee.com/",
        "code": code,
    }

    response = requests.post("https://keycloak.getrollee.com/realms/rollee/protocol/openid-connect/token",
                             body,
                             cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Fetching access token failed'}


def login(username: str, password: str):
    """
    Authenticate a user with the provided credentials to get the access token.
    """

    # Get initial cookie from KeyCloak
    url = "https://keycloak.getrollee.com/realms/rollee/protocol/openid-connect/auth?client_id=dashboard&redirect_uri=https://dashboard.getrollee.com/&response_type=code&scope=openid"
    response = requests.get(url)

    if response.status_code != 200:
        # If unable to fetch the cookie, extract the error message from the response HTML
        matches = parse_html(r'instruction">(.*?)<', response)
        message = matches.group(
            1) if matches else "we couldn't fetch cookie from KeyCloak"
        raise Exception(message)

    cookies = response.cookies

    # Parse the authenticate URL from the HTML body
    matches = parse_html(r'action="(.*?)"', response)

    if matches:
        authenticateUrl = matches.group(1)
    else:
        raise CustomException('authenticate URL not found', 500)

    body = {
        "username": username,
        "password": password
    }

    # Authenticate to the parsed form URL using the provided username & password
    # Allow_redirects=False to disable redirect to the dashboard, so we can get
    # the response without redirecting, so then we have Location header that we gonna use to get the access_token
    response = requests.post(html.unescape(authenticateUrl),  # Unescape the URL to obtain a properly formatted URL
                             body,
                             cookies=cookies,
                             allow_redirects=False)

    if response.status_code != 302:
        # If authentication fails, extract the error message from the response HTML
        if response.status_code == 200:
            matches = parse_html(r'alert__text">(.*?)<', response)
            if matches:
                raise CustomException('Invalid credentials', 401)
            raise CustomException("Login failed", 500)
        else:
            matches = parse_html(r'instruction">(.*?)<', response)
            message = matches.group(
                1) if matches else 'Login failed'
            raise CustomException(message, 500)

    # Extract the 'Location' header from the response to get the authorization 'code'
    location = response.headers.get('Location')
    if location is not None:
        code = location[location.index("code=")+5:len(location)]

        # After extracting the 'code', get the access token
        json = get_access_token(code, cookies)

        if 'error' in json:
            raise CustomException(json['error'], 500)

        return json

    else:
        raise CustomException('Location header not found', 500)
