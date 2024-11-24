from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from . import AzureAPI
from cryptography.fernet import Fernet
from django.conf import settings
import base64

# Generate a Fernet key using Django's SECRET_KEY
def get_fernet_key():
    # Use Django's SECRET_KEY to generate a base64 key for Fernet
    secret_key = settings.SECRET_KEY[:32]  # Make sure SECRET_KEY is at least 32 characters
    return base64.urlsafe_b64encode(secret_key.encode())

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        # Retrieve system content from environment variable
        system_content = os.getenv("SYSTEM_CONTENT", "default system content if not set")

        # Decrypt conversation history from cookies
        fernet = Fernet(get_fernet_key())
        encrypted_history = request.COOKIES.get("conversation_history", None)
        if encrypted_history:
            try:
                decrypted_history = fernet.decrypt(encrypted_history.encode()).decode()
                conversation_history = json.loads(decrypted_history)
            except Exception:
                conversation_history = []
        else:
            conversation_history = []

        # If no previous conversation history, add system content as the initial message
        if not conversation_history:
            conversation_history.append({"role": "system", "content": system_content})

        # Add the user message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Get assistant response from AzureAPI
        try:
            assistant_response = AzureAPI.Chat(conversation_history)
            # Add assistant's message to the conversation history
            conversation_history.append({"role": "assistant", "content": assistant_response})

            # Encrypt the conversation history before setting it in cookies
            encrypted_history = fernet.encrypt(json.dumps(conversation_history).encode()).decode()

            # Prepare JSON response and update conversation history in cookies
            response_data = JsonResponse({'response': assistant_response})
            response_data.set_cookie("conversation_history", encrypted_history, max_age=3600, httponly=True, secure=True)
            return response_data

        except Exception as e:
            return JsonResponse({"error": "Failed to retrieve response from API", "details": str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
