from constants import *
from helpers import format_name
from classes import Hitting

session_cookies = ''

def gc_init():
    # Load environment variables
    load_dotenv()

    # Set session cookies
    global session_cookies
    session_cookies = f'{CSRFTOKEN}={os.getenv(CSRFTOKEN)}; {SECURE_SESSIONID}={os.getenv(SECURE_SESSIONID)}; {SESSIONID}={os.getenv(SESSIONID)}'

def GET_hitting(session, session_cookies, team_id, start_ts, end_ts):
    HITTING_STATS = {}
    GET_batting_standard(session, session_cookies, team_id, start_ts, end_ts, HITTING_STATS)
    GET_batting_psp(session, session_cookies, team_id, start_ts, end_ts, HITTING_STATS)
    GET_batting_qabs(session, session_cookies, team_id, start_ts, end_ts, HITTING_STATS)
    return HITTING_STATS


def GET_batting_standard(session, session_cookies, team_id, start_ts, end_ts, HITTING_STATS):
    # Parse the "Batting Standard" page
    full_url = f'{BASE_URL}{STATS_URI}{team_id}/{BATTING_STANDARD}&start_ts={start_ts}&end_ts={end_ts}'
    payload = {}
    headers = {
        'Cookie': session_cookies
    }
    response = session.request("GET", full_url, headers=headers, data=payload)

    for player in response.json()['players']:
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


def GET_batting_psp(session, session_cookies, team_id, start_ts, end_ts, HITTING_STATS):
    # Parse the "Patience, Speed, & Power" page
    full_url = f'{BASE_URL}{STATS_URI}{team_id}/{BATTING_PSP}&start_ts={start_ts}&end_ts={end_ts}'
    payload = {}
    headers = { 
        'Cookie': session_cookies
    }
    response = session.request("GET", full_url, headers=headers, data=payload)

    for player in response.json()['players']:
        player_name = format_name(player['row_info']['player_name'])
        player_stats = HITTING_STATS[player_name]
        stats_inputted = 0
        for stat in player['stats']:
            if stat['identifier']['key'] == 'SB':
                player_stats.sb = stat['value']
                stats_inputted += 1
            elif stat['identifier']['key'] == 'CS':
                player_stats.cs = stat['value']
                stats_inputted += 1

            if stats_inputted >= 2:
                break


def GET_batting_qabs(session, session_cookies, team_id, start_ts, end_ts, HITTING_STATS):
    # Parse the "QABs & Team Impact" page
    full_url = f'{BASE_URL}{STATS_URI}{team_id}/{BATTING_QABS}&start_ts={start_ts}&end_ts={end_ts}'
    payload = {}
    headers = { 
        'Cookie': session_cookies
    }
    response = session.request("GET", full_url, headers=headers, data=payload)

    for player in response.json()['players']:
        player_name = format_name(player['row_info']['player_name'])
        player_stats = HITTING_STATS[player_name]
        stats_inputted = 0
        for stat in player['stats']:
            if stat['identifier']['key'] == 'SHB':
                player_stats.sac_b = stat['value']
                stats_inputted += 1
            elif stat['identifier']['key'] == 'SHF':
                player_stats.sac_f = stat['value']
                stats_inputted += 1

            if stats_inputted >= 2:
                break