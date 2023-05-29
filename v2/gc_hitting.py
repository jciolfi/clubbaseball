from constants import *
from helpers import *
from classes import Hitting

# return a dictionary of {str} -> {Hitting} that holds a player name and their hitting stats
def GET_hitting(session, session_cookies, team_id, start_ts, end_ts):
    # parse necessary tables to populate hitting stats for each player
    hitting_stats = {}
    GET_batting_standard(session, session_cookies, team_id, start_ts, end_ts, hitting_stats)
    GET_batting_psp(session, session_cookies, team_id, start_ts, end_ts, hitting_stats)
    GET_batting_qabs(session, session_cookies, team_id, start_ts, end_ts, hitting_stats)
    return hitting_stats


# parse the "Batting Standard" page
def GET_batting_standard(session, session_cookies, team_id, start_ts, end_ts, hitting_stats):
    # send request for stats
    url = build_stat_url(team_id, BATTING_STANDARD, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract AB, R, H, 2B, 3B, HR, RBI, BB, SO, HBP
    for player in players_stats:
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
        
        hitting_stats[player_name] = player_hitting


# Parse the "Patience, Speed, & Power" page
def GET_batting_psp(session, session_cookies, team_id, start_ts, end_ts, hitting_stats):
    # send request for stats
    url = build_stat_url(team_id, BATTING_PSP, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract SB and CS
    for player in players_stats:
        player_name = format_name(player['row_info']['player_name'])
        player_stats = hitting_stats[player_name]
        stats_inputted = 0
        for stat in player['stats']:
            if stat['identifier']['key'] == 'SB':
                player_stats.sb = int(stat['value'])
                stats_inputted += 1
            elif stat['identifier']['key'] == 'CS':
                player_stats.cs = int(stat['value'])
                stats_inputted += 1

            if stats_inputted >= 2:
                break


# Parse the "QABs & Team Impact" page
def GET_batting_qabs(session, session_cookies, team_id, start_ts, end_ts, hitting_stats):
    # send request for stats
    url = build_stat_url(team_id, BATTING_QABS, start_ts, end_ts)
    players_stats = get_players_stats(session, url, session_cookies)

    # extract SHB and SHF
    for player in players_stats:
        player_name = format_name(player['row_info']['player_name'])
        player_stats = hitting_stats[player_name]
        stats_inputted = 0
        for stat in player['stats']:
            if stat['identifier']['key'] == 'SHB':
                player_stats.sac_b = int(stat['value'])
                stats_inputted += 1
            elif stat['identifier']['key'] == 'SHF':
                player_stats.sac_f = int(stat['value'])
                stats_inputted += 1

            if stats_inputted >= 2:
                break