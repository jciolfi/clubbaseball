from constants import *

def format_name(name: str):
    if ' ' not in name:
        return name
    split = name.index(' ')
    return f'{name[split+1:]}, {name[:split]}'

def build_stat_url(team_id, stat_params, start_ts, end_ts):
    url = f'{BASE_URL}{STATS_URI}{team_id}/{stat_params}'
    if start_ts:
        url += f'&start_ts={start_ts}'
    if end_ts:
        url += f'&end_ts={end_ts}'

    return url