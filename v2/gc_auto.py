import requests, os, re, sys
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from constants import *

session_cookies = ''

def gc_init():
    # Load environment variables
    load_dotenv()

    # Set session cookies
    global session_cookies
    session_cookies = f'{CSRFTOKEN}={os.getenv(CSRFTOKEN)}; {SECURE_SESSIONID}={os.getenv(SECURE_SESSIONID)}; {SESSIONID}={os.getenv(SESSIONID)}'

def GET_login(session):
    payload={}
    headers = {
        'Cookie': session_cookies
    }

    resp = session.request("GET", BASE_URL + LOGIN_URI, headers=headers, data=payload)
    print(resp)
    print(resp.text)
    print(resp.headers)

    csrfmiddlewaretoken_pattern = re.compile(r"name='csrfmiddlewaretoken' value='([A-Za-z0-9]+)'")
    try:
        csrfmiddlewaretoken = csrfmiddlewaretoken_pattern.findall(resp.text)[0]
        return csrfmiddlewaretoken
    except IndexError:
        print(resp.text)
        raise LookupError('Could not find csrfmiddlewaretoken in login page')
    

def POST_login(session, csrfmiddlewaretoken):
    # payload = f'{CSRFMIDDLEWARETOKEN}={os.getenv(CSRFMIDDLEWARETOKEN)}&{EMAIL}={os.getenv(EMAIL)}&{PASSWORD}={os.getenv(PASSWORD)}'
    payload = f'{CSRFMIDDLEWARETOKEN}={csrfmiddlewaretoken}&{EMAIL}={os.getenv(EMAIL)}&{PASSWORD}={os.getenv(PASSWORD)}'
    headers = {
        'Referer': 'https://gc.com/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': session_cookies
    }
    
    response = session.request('POST', BASE_URL + DO_LOGIN_URI, headers=headers, data=payload)
    print(f'login: {response}')
    print(response.headers)

def POST_logout(session, csrfmiddlewaretoken):
    payload = f'{CSRFMIDDLEWARETOKEN}={csrfmiddlewaretoken}'
    headers = {
        'Referer': 'https://gc.com/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': session_cookies
    }
    response = session.request("POST", BASE_URL + DO_LOGOUT_URI, headers=headers, data=payload)
    print(f'logout: {response}')
    print(response.headers)

def GET_stats(session, url):
    if not url:
        print('Invalid GameChanger URL specified')
        sys.exit(0)
    
    parsed = urlparse(url)
    path_parts = parsed.path.split('/')
    try:
        team_id = path_parts[-2]
        team_id = team_id[team_id.rfind('-') + 1:]
    except IndexError:
        print('Could not find team ID')
        sys.exit(0)
    

    
    query_parts = parse_qs(parsed.query)
    start_ts = query_parts.get('start_ts', [None])[0]
    end_ts = query_parts.get('end_ts', [None])[0]

    print(f'team_id={team_id}, start_ts={start_ts}, end_ts={end_ts}')




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Must specify stats link to pull from. For example:')
        print(f'  python gc_auto.py "https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats?start_ts=1682866800&end_ts=1682866800"')
        sys.exit(0)

    gc_init()

    with requests.Session() as session:
        # csrfmiddlewaretoken = GET_login(session)
        # print(csrfmiddlewaretoken)
        # POST_login(session, csrfmiddlewaretoken)
        # POST_logout(session, csrfmiddlewaretoken)
        GET_stats(session, sys.argv[1])