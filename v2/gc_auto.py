import os, re, sys, csv
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from constants import *
from classes import *
from helpers import *
from gc_hitting import GET_hitting
from gc_pitching import GET_pitching

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

    csrfmiddlewaretoken_pattern = re.compile(r"name='csrfmiddlewaretoken' value='([A-Za-z0-9]+)'")
    try:
        csrfmiddlewaretoken = csrfmiddlewaretoken_pattern.findall(resp.text)[0]
        return csrfmiddlewaretoken
    except IndexError:
        print('Could not find csrfmiddleware token in /login. Continuing, but stats may be wrong')
        print('I am going to hope that you are already logged in.')
        return None
    

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

    hitting_stats = GET_hitting(session, session_cookies, team_id, start_ts, end_ts)
    print(hitting_stats)

    print('\n\n\n')

    pitching_stats = GET_pitching(session, session_cookies, team_id, start_ts, end_ts)
    print(pitching_stats)

    return hitting_stats, pitching_stats


def write_hitting_stats(filename, hitting_stats):
    if not filename:
        filename = 'output_hitting.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'SAC_F', 'SAC_B', 'HBP'])

        hitters = list(hitting_stats.keys())
        hitters.sort()

        for player in hitters:
            stats = hitting_stats[player]
            writer.writerow([player,
                             stats.ab, 
                             stats.r, 
                             stats.h, 
                             stats.doubles, 
                             stats.triples, 
                             stats.hr, 
                             stats.rbi, 
                             stats.bb,
                             stats.ibb,
                             stats.so,
                             stats.sb,
                             stats.cs,
                             stats.sac_f,
                             stats.sac_b,
                             stats.hbp])


def write_pitching_stats(filename, pitching_stats):
    if not filename:
        filename = 'output_pitching.csv'
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Started', 'W', 'L', 'CG', 'SHO', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'HBP', 'BB', 'IBB', 'SO', 'BK', 'WP', 'PK'])

        pitchers = list(pitching_stats.keys())
        pitchers.sort()

        for player in pitchers: 
            stats = pitching_stats[player]
            writer.writerow([player,
                             stats.started,
                             stats.w,
                             stats.l,
                             stats.cg,
                             stats.sho,
                             stats.sv,
                             stats.svo, 
                             stats.ip,
                             stats.h,
                             stats.r, 
                             stats.er, 
                             stats.hr, 
                             stats.hbp, 
                             stats.bb, 
                             stats.ibb, 
                             stats.so, 
                             stats.bk, 
                             stats.wp, 
                             stats.pk])