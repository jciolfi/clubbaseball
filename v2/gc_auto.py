import os, re, sys, csv
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from constants import *
from classes import *
from helpers import *
from gc_hitting import GET_hitting
from gc_pitching import GET_pitching

session_cookies = ''

# initialize session cookies from .env
def gc_init():
    # load environment variables
    load_dotenv()

    # set session cookies
    global session_cookies
    session_cookies = f'{SECURE_SESSIONID}={os.getenv(SECURE_SESSIONID)}; {SESSIONID}={os.getenv(SESSIONID)}'


# perform GET to /login: set the csrftoken, and return the csrfmiddlewaretoken
def GET_login(session):
    # send request to /login
    global session_cookies
    payload={}
    headers = { 'Cookie': session_cookies }
    response = session.request("GET", BASE_URL + LOGIN_URI, headers=headers, data=payload)

    # find csrftoken
    csrftoken_pattern = re.compile(r"csrftoken=([A-Za-z0-9]+);")
    for header, value in response.headers.items():
        if header == 'Set-Cookie':
            try:
                print(f'\n{header}: {value}\n')

                csrftoken = csrftoken_pattern.findall(value)[0]
                session_cookies = f'{CSRFTOKEN}={csrftoken}; {session_cookies}'
                print(f'SESSION_COOKIES: {session_cookies}')
                break
            except IndexError:
                print('Could not find csrftoken token in /login.')
                print('If you are already logged in, there will not be an issue. Otherwise, the program may crash.')
                print('---------------------------------------------------------------------------------------')

    # find csrfmiddlewaretoken
    csrfmiddlewaretoken_pattern = re.compile(r"name='csrfmiddlewaretoken' value='([A-Za-z0-9]+)'")
    try:
        csrfmiddlewaretoken = csrfmiddlewaretoken_pattern.findall(response.text)[0]
        return csrfmiddlewaretoken
    except IndexError:
        print('Could not find csrfmiddleware token in /login.')
        print('If you are already logged in, there will not be an issue. Otherwise, the program may crash.')
        print('---------------------------------------------------------------------------------------')
        return None
    

# attempt to log into GameChanger Classic; if this fails, program is aborted
def POST_login(session, csrfmiddlewaretoken):
    # send request to POST /do-login
    payload = f'{CSRFMIDDLEWARETOKEN}={csrfmiddlewaretoken}&{EMAIL}={os.getenv(EMAIL)}&{PASSWORD}={os.getenv(PASSWORD)}'
    headers = {
        'Referer': 'https://gc.com/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': session_cookies
    }
    response = session.request('POST', BASE_URL + DO_LOGIN_URI, headers=headers, data=payload)

    # check for bad status (can't continue without authentication)
    if response.status_code != 200:
        print('Unable to log in. Are your email and password correct?')
        sys.exit(0)


# log out of the GameChanger Classic account
def POST_logout(session, csrfmiddlewaretoken):
    # send request to POST /do-logout
    payload = f'{CSRFMIDDLEWARETOKEN}={csrfmiddlewaretoken}'
    headers = {
        'Referer': 'https://gc.com/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': session_cookies
    }
    response = session.request("POST", BASE_URL + DO_LOGOUT_URI, headers=headers, data=payload)

    print(f'logout: {"Good" if response.status_code == 200 else "Bad"}')


# get hitting and pitching stats for the selected date range
def GET_stats(session, url):
    # check for invalid url
    if not url:
        print('Invalid GameChanger URL specified')
        sys.exit(0)
    
    # find the GameChanger defined team_id
    parsed = urlparse(url)
    path_parts = parsed.path.split('/')
    try:
        team_id = path_parts[-2]
        team_id = team_id[team_id.rfind('-') + 1:]
    except IndexError:
        print('Could not find team ID')
        sys.exit(0)
    
    # find the selected date range, if applicable
    query_parts = parse_qs(parsed.query)
    start_ts = query_parts.get('start_ts', [None])[0]
    end_ts = query_parts.get('end_ts', [None])[0]

    # get the hitting stats and print them
    hitting_stats = GET_hitting(session, session_cookies, team_id, start_ts, end_ts)
    print(hitting_stats)

    print('\n\n\n')

    # get the pitching stats and print them
    pitching_stats = GET_pitching(session, session_cookies, team_id, start_ts, end_ts)
    print(pitching_stats)

    return hitting_stats, pitching_stats


# write hitting stats to disk
def write_hitting_stats(filename, hitting_stats):
    # set default filename if none specified
    if not filename:
        filename = 'output_hitting.csv'

    with open(filename, mode='w', newline='') as file:
        # write headers
        writer = csv.writer(file)
        writer.writerow(['Name', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'BB', 'IBB', 'SO', 'SB', 'CS', 'SAC_F', 'SAC_B', 'HBP'])

        # sort alphabeticallly by last name
        hitters = list(hitting_stats.keys())
        hitters.sort()

        # write each hitter's stats to row
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


# write pitching stats to disk
def write_pitching_stats(filename, pitching_stats):
    # set default filename if none specified
    if not filename:
        filename = 'output_pitching.csv'
    
    with open(filename, mode='w', newline='') as file:
        # write headers
        writer = csv.writer(file)
        writer.writerow(['Name', 'Started', 'W', 'L', 'CG', 'SHO', 'SV', 'SVO', 'IP', 'H', 'R', 'ER', 'HR', 'HBP', 'BB', 'IBB', 'SO', 'BK', 'WP', 'PK'])

        # sort alphabeticallly by last name
        pitchers = list(pitching_stats.keys())
        pitchers.sort()

        # write each pitchers's stats to row
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