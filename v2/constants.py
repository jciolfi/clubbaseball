SECURE_SESSIONID = 'gcdotcom_secure_sessionid'
SESSIONID = 'gcdotcom_sessionid'
SET_COOKIE = 'Set-Cookie'
CSRFTOKEN = 'csrftoken'
CSRFMIDDLEWARETOKEN = 'csrfmiddlewaretoken'
EMAIL = 'email'
PASSWORD = 'password'
REFERER_VAL = 'https://gc.com/login'
LAST_VIEWED = 'last_team_viewed' # goes along with TEAM_ID

BASE_URL = 'https://gc.com'
LOGIN_URI = '/login'
DO_LOGIN_URI = '/do-login'
DO_LOGOUT_URI = '/do-logout'
STATS_URI = '/stats/team' # THIS NEEDS PATH PARAM /{team_id} as well. Get from user input
BATTING_STANDARD = '/?stats_requested=%5B%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22GP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22PA%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22H%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%221B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%222B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%223B%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22HR%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22RBI%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22R%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22HBP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22ROE%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22FC%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22CI%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22BB%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SO%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22AVG%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22OBP%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22SLG%22%7D%2C%7B%22category%22%3A%22offense%22%2C%22key%22%3A%22OPS%22%7D%5D&qualifying_stat=%7B%22key%22%3A%22GP%22%2C%22category%22%3A%22offense%22%7D&game_filter=Qualified'
BATTING_PSP = 
BATTING_QABS = 
PITCHING_STANDARD = 
PITCHING_COMMAND = 
PITCHING_BATTER = 
PITCHING_RUNS = 