import requests, os, re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from constants import *

session_cookies = {}

def gc_init():
    # Load environment variables
    load_dotenv()

    # Set session cookies
    session_cookies[SESSIONID] = os.getenv(SESSIONID)
    session_cookies[SECURE_SESSIONID] = os.getenv(SECURE_SESSIONID)

def GET_login(session):
    # Get base login page
    resp = session.get(BASE_URL + LOGIN_URI, cookies=session_cookies)

    # Set csrftoken in session headers
    resp_cookies = resp.headers[SET_COOKIE]
    if resp_cookies.startswith(CSRFTOKEN):
        session_cookies[CSRFTOKEN] = resp_cookies
    else:
        raise LookupError('Could not find csrftoken in login response headers')
    
    resp_content = resp.text
    csrfmiddlewaretoken_pattern = re.compile(r"name='csrfmiddlewaretoken' value='([A-Za-z0-9]+)'")
    try:
        csrfmiddlewaretoken = csrfmiddlewaretoken_pattern.findall(resp_content)[0]
        return csrfmiddlewaretoken
    except IndexError:
        raise LookupError('Could not find csrfmiddlewaretoken in login page')
    

def POST_login(session):
    resp = session.get(BASE_URL + DO_LOGIN_URI, cookies=session_cookies)




if __name__ == "__main__":
    gc_init()

    session = requests.Session()
    csrfmiddlewaretoken = GET_login(session)
    print(csrfmiddlewaretoken)