from rest_framework.decorators import api_view
from django.http import JsonResponse
from .solution import get_accounts_for_user
from .exceptions import CustomException


@api_view(['POST'])
def accounts_list(request):
    data = request.data

    # Check if the 'username' parameter is missing in the request data
    if 'username' not in data:
        return JsonResponse({'error': 'Username is missing'}, status=400)

    # Check if the 'password' parameter is missing in the request data
    if 'password' not in data:
        return JsonResponse({'error': 'Password is missing'}, status=400)

    # Check if the 'user_id' parameter is missing in the request data
    if 'user_id' not in data:
        return JsonResponse({'error': 'User ID is missing'}, status=400)

    try:
        # Retrieve accounts for the given user using the provided credentials details
        accounts = get_accounts_for_user(
            data.get('username'),
            data.get('password'),
            data.get('user_id'),
        )

        return JsonResponse({"accounts": [account.model_dump() for account in accounts]}, status=200)

    # If a CustomException is raised during the process, handle it with custom error message and status code
    except CustomException as e:
        return JsonResponse({'error': str(e)}, status=e.status_code)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
