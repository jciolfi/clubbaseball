import requests, os, re, sys
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from constants import *
from classes import *
from helpers import *

session_cookies = ''
HITTING_STATS = {}
PITCHING_STATS = {}

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

    # print(f'team_id={team_id}, start_ts={start_ts}, end_ts={end_ts}')
    GET_batting_standard(session, team_id, start_ts, end_ts)
    # GET_batting_psp(session, team_id, start_ts, end_ts)
    # GET_batting_qabs(session, team_id, start_ts, end_ts)

    # GET_pitching_standard(session, team_id, start_ts, end_ts)
    # GET_pitching_command(session, team_id, start_ts, end_ts)
    # GET_pitching_batter(session, team_id, start_ts, end_ts)
    # GET_pitching_runs(session, team_id, start_ts, end_ts)

# return true if successful. If successful move to next stat category in batting
def GET_batting_standard(session, team_id, start_ts, end_ts):
    full_url = f'{BASE_URL}{STATS_URI}{team_id}/{BATTING_STANDARD}'
    payload = {}
    headers = {
        'Cookie': session_cookies
    }
    response = requests.request("GET", full_url, headers=headers, data=payload)
    response_json = response.json()

    for player in response_json['players']:
        player_name = format_name(player['row_info']['player_name'])
        temp_stats = {}
        for stat in player['stats']:
            temp_stats[stat['identifier']['key']] = stat['value']

        player_hitting = Hitting()
        player_hitting.ab = int(temp_stats['AB'])
        player_hitting.r = int(temp_stats['R'])
        player_hitting.h = int(temp_stats['H'])
        player_hitting.doubles = int(temp_stats['2B'])
        player_hitting.triples = int(temp_stats['3B'])
        player_hitting.hr = int(temp_stats['HR'])
        player_hitting.rbi = int(temp_stats['RBI'])
        player_hitting.bb = int(temp_stats['BB'])
        player_hitting.so = int(temp_stats['SO'])
        player_hitting.hbp = int(temp_stats['HBP'])
        
        HITTING_STATS[player_name] = player_hitting
        print(HITTING_STATS)
        break


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