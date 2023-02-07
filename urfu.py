import requests
import prettytable
from prettytable import PrettyTable


url = "https://study-app.urfu.ru/api/auth/login"

headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "ustasapp/48 CFNetwork/1404.0.5 Darwin/22.3.0",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Basic ZXN4aWFvbG1lQGdtYWlsLmNvbTpxZG00YmpmLlBDRyp4enBAZXZu",
    "Cache-Control": "no-cache"
}

data = {"login": "YOUR EMAIL", "password": "YOUR PASSWORD"}

session = requests.Session()
response = session.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("[+] Login successful")
    token = response.json()["token"]
    headers["Authorization"] = "Bearer " + token
    url = "https://study-app.urfu.ru/api/users/me"
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        #print("GET request successful", response.status_code)
        json_data = response.json()
        table = prettytable.PrettyTable(hrules=prettytable.ALL)
        table = prettytable.PrettyTable(["Attribute", "Value"])
        table.add_row(["Last Name", json_data["lastName"]])
        table.add_row(["First Name", json_data["firstName"]])
        table.add_row(["Middle Name", json_data["middleName"]])
        for group in json_data["groups"]:
            table.add_row(["Group Title", group["title"]])
            table.add_row(["Group StartYear", group["startYear"]])
        print(table)
    else:
        print("GET request failed ", response.status_code)
else:
    print("Login failed")
    
headers["Authorization"] = "Bearer " + token
url = "https://study-app.urfu.ru/api/schedule/events?date=&tkey="
response = session.get(url, headers=headers)
if response.status_code == 200:
    #print("GET schedule/events request successful", response.status_code)
    #print(response.json())
    events = response.json()

    table = PrettyTable()
    table.field_names = ["Number","Teacher", "Event Date", "Start", "End", "Discipline", "Address", "Auditory"]
    num = 1

    for event in events:
        table.add_row([num, event['teacher']['name'], event['eventDate'], event['start'], event['end'], event['discipline'], event['address'], event['auditory']])
        num += 1

    print(table)
else:
    print("GET schedule/events request failed", response.status_code)
