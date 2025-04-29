import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.inference.models import SystemMessage, UserMessage

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

# Print environment variables to verify
print("AZURE_ENDPOINT:", AZURE_ENDPOINT)
print("AZURE_KEY:", AZURE_KEY)

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_KEY"]),
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is deeplearning?"),
    ],
    model="DeepSeek-R1"  # Specify the model parameter
)

print("Response:", response.choices[0].message.content)
