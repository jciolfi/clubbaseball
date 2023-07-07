import os, re, sys, csv, requests
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from constants import *
from classes import *
from helpers import *
from gc_hitting import GET_hitting
from gc_pitching import GET_pitching

session_cookies = ''
csrfmiddlewaretoken = ''

# initialize session cookies from .env
def gc_init():
    # load environment variables
    load_dotenv()


    
def TEST_john(session):
    global session_cookies
    global csrfmiddlewaretoken

    response = session.request('GET', BASE_URL + LOGIN_URI)

    csrftoken_pattern = re.compile(r"csrftoken=([A-Za-z0-9]+);")
    csrfmiddlewaretoken_pattern = re.compile(r"name='csrfmiddlewaretoken' value='([A-Za-z0-9]+)'")
    try:
        # find csrftoken
        set_cookie = response.headers['Set-Cookie']
        csrftoken = csrftoken_pattern.findall(set_cookie)[0]
        session_cookies = f'{CSRFTOKEN}={csrftoken}'

        # find csrfmiddlewaretoken
        csrfmiddlewaretoken = csrfmiddlewaretoken_pattern.findall(response.text)[0]
    except KeyError:
        print('Could not find Set-Cookie to look for csrftoken. Aborting...')
        exit(1)
    except IndexError:
        print('Could not find both csrftoken and csrfmiddlewaretoken. Aborting...')
        exit(1)


    payload = f'csrfmiddlewaretoken={csrfmiddlewaretoken}&email={os.getenv(EMAIL)}&password={os.getenv(PASSWORD)}'
    headers = {
        'Referer': 'https://gc.com/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'csrftoken={csrftoken}'
    }

    response = requests.request('POST', BASE_URL + DO_LOGIN_URI, headers=headers, data=payload)
    secure_sessionid_pattern = re.compile(r"gcdotcom_secure_sessionid=([A-Za-z0-9]+);")
    sessionid_pattern = re.compile(r"gcdotcom_sessionid=([A-Za-z0-9]+);")
    try:
        set_cookie = response.headers['Set-Cookie']
        secure_sessionid = secure_sessionid_pattern.findall(set_cookie)[0]
        sessionid = sessionid_pattern.findall(set_cookie)[0]
        session_cookies += f'; {SECURE_SESSIONID}={secure_sessionid}; {SESSIONID}={sessionid}'
    except KeyError:
        print('Could not find Set-Cookie to look for session ids. Aborting...')
        exit(1)
    except IndexError:
        print('Found Set-Cookie, but could not find session ids. Aborting...')
        exit(1)

    
    print(f'SESSION COOKIES SET: {session_cookies}')


# log out of the GameChanger Classic account
def POST_logout(session):
    # send request to POST /do-logout
    payload = f'{CSRFMIDDLEWARETOKEN}={csrfmiddlewaretoken}'
    headers = {
        'Referer': 'https://gc.com/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': session_cookies
    }
    response = session.request("POST", BASE_URL + DO_LOGOUT_URI, headers=headers, data=payload)

    print(f'logout: {"Logged out" if response.status_code == 200 else "Stayed logged in"}')


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
            

if __name__ == "__main__":
    gc_init()
    with requests.Session() as session:
        TEST_john(session)
        POST_logout(session)