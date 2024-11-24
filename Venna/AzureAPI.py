from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os

def get_azure_key():
    """Retrieve the Azure API key from an environment variable."""
    return os.getenv("AZURE_KEY")  # Correct usage to fetch the key from environment variables

def Chat(conversation_history):
    # Retrieve the API key and endpoint from the environment or secure store
    print("its here")
    api_key = get_azure_key()
    endpoint = os.getenv("AZURE_ENDPOINT", "https://Meta-Llama-3-1-405B-venna.eastus2.models.ai.azure.com")  # Ensure the endpoint is also in environment variables

    if not api_key or not endpoint:
        raise Exception("API key and endpoint must be provided to connect to the endpoint.")

    # Initialize client
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )

    # Prepare payload with full conversation history
    payload = {
        "messages": conversation_history,
        "max_tokens": 2048,
        "temperature": 0.8,
        "top_p": 0.1,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    # Get the response from the model
    response = client.complete(payload)
    assistant_message = response.choices[0].message["content"]

    return assistant_message
