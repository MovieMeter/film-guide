import requests


url = 'http://ipecho.net/plain'
proxies = {
    'http': 'http://10.11.0.1:8080',
    'https': 'https://10.11.0.1:8080'
}
# r = requests.get(url, proxies=proxies)
r = requests.get(url)
print(r.text)
