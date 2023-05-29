from constants import *
from helpers import *
from classes import Pitching

def GET_pitching(session, session_cookies, team_id, start_ts, end_ts):
    pitching_stats = {}
    GET_pitching_standard(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    GET_pitching_command(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    GET_pitching_batter(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    GET_pitching_runs(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    return pitching_stats


def GET_pitching_standard(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    full_url = build_stat_url(team_id, PITCHING_STANDARD, start_ts, end_ts)
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

        player_pitching = Pitching()
        player_pitching.started = int(temp_stats['GS'])
        player_pitching.w = int(temp_stats['W'])
        player_pitching.l = int(temp_stats['L'])
        player_pitching.sv = int(temp_stats['SV'])
        player_pitching.svo = int(temp_stats['SVO'])
        outs = int(temp_stats['outs'])
        player_pitching.ip = f'{outs // 3}.{outs % 3}'
        player_pitching.h = int(temp_stats['H'])
        player_pitching.r = int(temp_stats['R'])
        player_pitching.er = int(temp_stats['ER'])
        player_pitching.hbp = int(temp_stats['HBP'])
        player_pitching.bb = int(temp_stats['BB'])
        player_pitching.so = int(temp_stats['SO'])

        pitching_stats[player_name] = player_pitching


def GET_pitching_command(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    full_url = build_stat_url(team_id, PITCHING_COMMAND, start_ts, end_ts)
    payload = {}
    headers = {
        'Cookie': session_cookies
    }
    response = session.request("GET", full_url, headers=headers, data=payload)

    for player in response.json()['players']:
        player_name = format_name(player['row_info']['player_name'])
        for stat in player['stats']:
            if stat['identifier']['key'] == 'WP':
                pitching_stats[player_name].wp = int(stat['value'])
                break
        
        

def GET_pitching_batter(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    full_url = build_stat_url(team_id, PITCHING_BATTER, start_ts, end_ts)
    payload = {}
    headers = {
        'Cookie': session_cookies
    }
    response = session.request("GET", full_url, headers=headers, data=payload)

    for player in response.json()['players']:
        player_name = format_name(player['row_info']['player_name'])
        for stat in player['stats']:
            if stat['identifier']['key'] == 'HR':
                pitching_stats[player_name].hr = int(stat['value'])
                break

def GET_pitching_runs(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    full_url = build_stat_url(team_id, PITCHING_RUNS, start_ts, end_ts)
    payload = {}
    headers = {
        'Cookie': session_cookies
    }
    response = session.request("GET", full_url, headers=headers, data=payload)

    for player in response.json()['players']:
        player_name = format_name(player['row_info']['player_name'])
        stats_inputted = 0
        for stat in player['stats']:
            if stat['identifier']['key'] == 'BK':
                pitching_stats[player_name].bk = int(stat['value'])
                stats_inputted += 1
            elif stat['identifier']['key'] == 'PK':
                pitching_stats[player_name].pk = int(stat['value'])
                stats_inputted += 1
            
            if stats_inputted >= 2:
                break