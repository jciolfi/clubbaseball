import requests, os, re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from constants import *

session_cookies = {}

def gc_init():
    # Load environment variables
    load_dotenv()

    # Set session cookies
    session_cookies[CSRFTOKEN] = os.getenv(CSRFTOKEN.upper())
    session_cookies[SESSIONID] = os.getenv(SESSIONID)
    session_cookies[SECURE_SESSIONID] = os.getenv(SECURE_SESSIONID)

def GET_login(session):
    # Get base login page
    resp = session.get(BASE_URL + LOGIN_URI, cookies=session_cookies)

    # # Set csrftoken in session headers
    # resp_cookies = resp.headers[SET_COOKIE]
    # if resp_cookies.startswith(CSRFTOKEN):
    #     session_cookies[CSRFTOKEN] = resp_cookies
    # else:
    #     raise LookupError('Could not find csrftoken in login response headers')
    
    resp_content = resp.text
    csrfmiddlewaretoken_pattern = re.compile(r"name='csrfmiddlewaretoken' value='([A-Za-z0-9]+)'")
    try:
        csrfmiddlewaretoken = csrfmiddlewaretoken_pattern.findall(resp_content)[0]
        return csrfmiddlewaretoken
    except IndexError:
        raise LookupError('Could not find csrfmiddlewaretoken in login page')
    

def POST_login(session, csrfmiddlewaretoken):
    # content_length = len(f'username={os.getenv(EMAIL)}&password={os.getenv(PASSWORD)}&csrfmiddlewaretoken={csrfmiddlewaretoken}')


    form_data = {
        CSRFMIDDLEWARETOKEN: csrfmiddlewaretoken,
        EMAIL: os.getenv(EMAIL),
        PASSWORD: os.getenv(PASSWORD)
    }
    headers = {
        REFERER: REFERER_VAL,
        'Host': 'gc.com',
        'User-Agent': 'PostmanRuntime/7.29.2',
        'Postman-Token': '17a8687d-30d9-42de-88c6-77e7b03b0b89'
    }
    # request = requests.Request('POST', BASE_URL + DO_LOGIN_URI, data=form_data, headers=headers, cookies=session_cookies)
    # prepared_request = request.prepare()

    # # Print the request details
    # print(f"URL: {prepared_request.url}")
    # print(f"Method: {prepared_request.method}")
    # print("Headers:")
    # for header, value in prepared_request.headers.items():
    #     print(f"{header}: {value}")
    # print("Body:")
    # print(prepared_request.body)

    resp = session.post(BASE_URL + DO_LOGIN_URI, headers=headers, cookies=session_cookies, data=form_data)
    print(resp)
    print(resp.request.headers)


def GET_stat_page(session, url):
    headers = {
        'Host': 'gc.com',
        'User-Agent': 'PostmanRuntime/7.29.2',
        'Postman-Token': '60a94a88-1d6e-42b9-ac1e-a6a75f2bcd82',
        'Cookie': 'csrftoken=DHbNdmXhqQi3pOJZBz20fV0jdZbSFNkZwKf5TRRf6TbSNiPiyGbRN2AFNS5QG350; gcdotcom_secure_sessionid=6nxjslbh0mmkwe2fkusewk0l38ee44jv; gcdotcom_sessionid=hyw8debutvrcj46x4eh6u0p1vhm39k47'
    }

    resp = session.get(url, headers=headers)
    print(resp.text)



if __name__ == "__main__":
    gc_init()

    with requests.Session() as session:
        # csrfmiddlewaretoken = GET_login(session)
        # # csrfmiddlewaretoken = 'b1LMjhbeyMvyl6ieYmgsqqfciB6D3WJL44P4ZM5cePonJAoxVtpjYxPySu0B4cuM'
        # # print(csrfmiddlewaretoken)
        # # print(session_cookies)
        # POST_login(session, csrfmiddlewaretoken)
        GET_stat_page(session, 'https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats?start_ts=1682866800')