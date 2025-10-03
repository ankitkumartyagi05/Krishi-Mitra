import requests

url = "https://open-ai21.p.rapidapi.com/conversationllama"

payload = {
	"messages": [
		{
			"role": "user",
			"content": "hello"
		}
	],
	"web_access": False
}
headers = {
	"x-rapidapi-host": "open-ai21.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())