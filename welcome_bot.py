import requests
from datetime import datetime, timedelta

API_URL = "https://az.wikipedia.org/w/api.php"
USERNAME = "TarantulaBot"
PASSWORD = "@tlsp2007@"

def login():
    # Token alma
    r1 = requests.get(API_URL, params={
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json'
    })
    login_token = r1.json()['query']['tokens']['logintoken']

    # Login ol
    r2 = requests.post(API_URL, data={
        'action': 'login',
        'lgname': USERNAME,
        'lgpassword': PASSWORD,
        'lgtoken': login_token,
        'format': 'json'
    })
    return r2.cookies

def get_recent_users():
    now = datetime.utcnow()
    past = now - timedelta(minutes=1)
    r = requests.get(API_URL, params={
        'action': 'query',
        'list': 'recentchanges',
        'rcstart': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'rcend': past.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'rctype': 'new',
        'rcprop': 'user',
        'format': 'json'
    })
    changes = r.json().get('query', {}).get('recentchanges', [])
    return [change['user'] for change in changes]

def welcome_user(user, cookies):
    # CSRF token
    r1 = requests.get(API_URL, params={
        'action': 'query',
        'meta': 'tokens',
        'format': 'json'
    }, cookies=cookies)
    csrf_token = r1.json()['query']['tokens']['csrftoken']

    # Redaktə et
    page_title = f"İstifadəçi_müzakirəsi:{user}"
    text = "{{Xoşgəldiniz}} ~~~~"
    summary = "Vikipediyaya xoş gəldiniz!"

    requests.post(API_URL, data={
        'action': 'edit',
        'title': page_title,
        'appendtext': text,
        'summary': summary,
        'token': csrf_token,
        'format': 'json'
    }, cookies=cookies)

def main():
    cookies = login()
    users = get_recent_users()
    for user in users:
        welcome_user(user, cookies)

if __name__ == "__main__":
    main()
