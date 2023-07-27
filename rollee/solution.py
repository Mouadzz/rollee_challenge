import requests
from .account import Account
from .login import login
from .exceptions import CustomException
from .models import User, Platform, AccountRecord, Profile, Vehicle


def parse_accounts(json):
    """
    Parse the JSON response, extract and save accounts to db.
    """
    accounts = []
    user, _ = User.objects.get_or_create(id=json['user']['id'])

    for account_json in json['user']['accounts']:
        platform, _ = Platform.objects.get_or_create(
            id=account_json['platform']['id'],
            defaults={
                'name': account_json['platform']['name'],
                'logo': account_json['platform']['logo']
            }
        )

        account, created = AccountRecord.objects.update_or_create(
            id=account_json['id'],
            user=user,
            defaults={
                'name': account_json['name'],
                'status': account_json['status'],
                'avatar': account_json['avatar'],
                'email': account_json['email'],
                'platform': platform,
                'country': account_json['country'],
                'last_update': account_json['last_update'],
                'currency': account_json['currency'],
                'gross_earnings': account_json['gross_earnings'],
                'net_amount': account_json['net_amount'],
                'taxes': account_json['taxes'],
                'bonus_amount': account_json['bonus_amount'],
                'platform_fee': account_json['platform_fee'],
                'activity': account_json['activity'],
                'trips': account_json['trips'],
                'employment': account_json['employment'],
                'documents': account_json['documents']
            },
        )

        # delete profile and vehicles in case account already exists,
        # so then we can create new ones
        if not created:
            account.vehicles.all().delete()
            if hasattr(account, 'profile'):
                account.profile.delete()

        # create new profile for the account
        Profile.objects.create(
            account=account,
            first_name=account_json['profile']['first_name'],
            last_name=account_json['profile']['last_name'],
            full_name=account_json['profile']['full_name'],
            phone=account_json['profile']['phone'],
            email=account_json['profile']['email'],
            image_url=account_json['profile']['image_url'],
            street=account_json['profile']['street'],
            zip=account_json['profile']['zip'],
            country_phone_code=account_json['profile']['country_phone_code'],
            licence_number=account_json.get('licence_number', None),
            licence_expire_dt=account_json.get('licence_expire_dt', None)
        )

        # create new vehicles for the account
        for vehicle in account_json['vehicles']:
            Vehicle.objects.create(
                account=account,
                make=vehicle['make'],
                model=vehicle['model'],
                year=vehicle['year'],
                license_plate=vehicle['license_plate']
            )

        new_account = Account(
            account_id=str(account.id),
            name=account.name,
            email=account.email,
            platform_name=account.platform.name,
            country=account.country,
            currency=account.currency,
            gross_earnings=account.gross_earnings
        )
        accounts.append(new_account)
    return accounts


def retrieve_accounts(headers, user_id):
    # Fetch all users
    response = requests.get(
        "https://api.sand.getrollee.com/api/dashboard/v0.1/users?start_date=1689548400&end_date=1690153199&limit=10000&cursor=0",
        headers=headers
    )

    if (response.status_code == 200):
        json = response.json()
        for user_json in json['users']:
            if (user_id == user_json['id']):
                # Fetch user details
                url = f"https://api.sand.getrollee.com/api/dashboard/v0.1/views/user/{user_id}?start_date=1689548400&end_date=1690153199"
                response = requests.get(
                    url,
                    headers=headers
                )
                accounts = parse_accounts(response.json())
                return accounts

        raise CustomException('User not found', 404)

    elif response.status_code == 401:
        raise CustomException('Unauthorized', 401)
    else:
        raise CustomException('Unknown error', 500)


def get_accounts_for_user(username: str, password: str, user_id: str) -> list[Account]:
    """Your solution here"""
    try:
        # Perform user login and get the JSON token
        json_token = login(username=username, password=password)

        # Prepare the Authorization header with the obtained token
        headers = {
            'Authorization': json_token['token_type'] + ' ' + json_token['access_token']
        }

        accounts = retrieve_accounts(headers, user_id)
        return accounts

    except CustomException as e:
        raise e
    except Exception as e:
        raise e
