import requests

url = "https://gc.com/do-login"

payload='csrfmiddlewaretoken=YI3HyqQJjbG0CcS4SlTsmicdEcw33USLRL7ZeVKHZezP0GYnPs2jUpMze5q14aDM&email=ciolfi.j%40northeastern.edu&password=Iwbaamsd347%26g'
headers = {
  'Referer': 'https://gc.com/login',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'csrftoken=DHbNdmXhqQi3pOJZBz20fV0jdZbSFNkZwKf5TRRf6TbSNiPiyGbRN2AFNS5QG350; gcdotcom_secure_sessionid=6nxjslbh0mmkwe2fkusewk0l38ee44jv; gcdotcom_sessionid=hyw8debutvrcj46x4eh6u0p1vhm39k47; last_team_viewed=640424614cea87ae8c000001'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
