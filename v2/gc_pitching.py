from constants import *
from helpers import *
from classes import Pitching

# return a dictionary of {str} -> {Pitching} that holds a player name and their pitching stats
def GET_pitching(session, session_cookies, team_id, start_ts, end_ts):
    # parse necessary tables to populate pitching stats for each player
    pitching_stats = {}
    GET_pitching_standard(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    GET_pitching_command(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    GET_pitching_batter(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    GET_pitching_runs(session, session_cookies, team_id, start_ts, end_ts, pitching_stats)
    return pitching_stats


# parse stats from the "Pitching -> Standard" tab
def GET_pitching_standard(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    # get player stats for pitching standard; expect json response
    url = build_stat_url(team_id, PITCHING_STANDARD, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract GS, W, L, SV, SVO, IP, H, R, ER, HBP, BB, SO
    for player in players_stats:
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


# parse stats from the "Pitching -> Command" tab
def GET_pitching_command(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    # get player stats for pitching command; expect json response
    url = build_stat_url(team_id, PITCHING_COMMAND, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract WP
    for player in players_stats:
        player_name = format_name(player['row_info']['player_name'])
        for stat in player['stats']:
            if stat['identifier']['key'] == 'WP':
                pitching_stats[player_name].wp = int(stat['value'])
                break
        
        
# parse stats from the "Pitching -> Batter Results" tab
def GET_pitching_batter(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    # get player stats for pitching batter results; expect json response
    url = build_stat_url(team_id, PITCHING_BATTER, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract HR
    for player in players_stats:
        player_name = format_name(player['row_info']['player_name'])
        for stat in player['stats']:
            if stat['identifier']['key'] == 'HR':
                pitching_stats[player_name].hr = int(stat['value'])
                break


# parse stats from the "Pitching -> Runs & Running Game" tab
def GET_pitching_runs(session, session_cookies, team_id, start_ts, end_ts, pitching_stats):
    # get player stats for pitching runs & running game; expect json response
    url = build_stat_url(team_id, PITCHING_RUNS, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract BK and PIK
    for player in players_stats:
        player_name = format_name(player['row_info']['player_name'])
        stats_inputted = 0
        for stat in player['stats']:
            if stat['identifier']['key'] == 'BK':
                pitching_stats[player_name].bk = int(stat['value'])
                stats_inputted += 1
            elif stat['identifier']['key'] == 'PIK':
                pitching_stats[player_name].pk = int(stat['value'])
                stats_inputted += 1
            
            if stats_inputted >= 2:
                break