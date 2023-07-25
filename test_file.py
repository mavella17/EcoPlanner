import requests

API_KEY = 'UeGSxzCjymyaVVhbNlZYkQ'
url = "https://www.carboninterface.com/api/v1/estimates"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    print(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")