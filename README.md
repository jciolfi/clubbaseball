# clubbaseball

## v1 (Deprecated)
Need to copy/paste stats tables from "Season Stats" tab into the corresponding variables. Must log in on your own in a browser, navigate to the tab, and select the stat range (typically one game at a time) for 
- Hitting stat tables: "Standard", "Patience, Speed & Power", "QABs & Team Impact"
- Pitching stat tables: "Standard", "Command", "Batter Results", "Runs & Running Game"

## v2
### .env
Create a filename called `.env` in the `v2` folder. Copy and paste the following into it:
gcdotcom_secure_sessionid=
gcdotcom_sessionid=
csrftoken=
last_team_viewed=640424614cea87ae8c000001
email=
password=

Fill out these values. Your email and password are what you use to log onto GameChanger. 

Your gcdotcom_secure_sessionid, gcdotcom_sessionid, and csrftoken can be found by doing the following:
1. Open the developer tools (F12 in chrome)
2. Navigate to the "Network" tab
3. Select "Doc"
4. Navigate to https://gc.com/login
5. Select the entry that says "login"
6. Scroll and expand the Request Headers menu.
7. Copy the values for `csrftoken=...`, `gcdotcom_secure_sessionid=...`, `gcdotcom_sessionid=...`
8. Paste the respective values into the .env

