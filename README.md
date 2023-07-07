# clubbaseball

## v1 (Deprecated)
Need to copy/paste stats tables from "Season Stats" tab into the corresponding variables. Must log in on your own in a browser, navigate to the tab, and select the stat range (typically one game at a time) for 
- Hitting stat tables: "Standard", "Patience, Speed & Power", "QABs & Team Impact"
- Pitching stat tables: "Standard", "Command", "Batter Results", "Runs & Running Game"

## v2
This is a more automated option. It will log in for you and output the same information with you doing less work. All you need to do is the setup, and then you are good to go.

### .env
Create a filename called `.env` in the `v2` folder. Copy and paste the following into it:

```
email=
password=
```

Your email and password are what you use to log onto GameChanger. 

### Instructions to Execute the Program
1. Navigate to GameChanger Classic. Log in and select the "Season Stats" tab. Select the appropriate date range
2. Copy the URL in the top bar.
3. Change your directory into where /clubbaseball/v2 is located.
4. Type "python main.py <your_copied_url>".
5. If you would like to name the output spreadsheets, you can do so by appending "--hit <name>" and "--pitch <name>"'. If you do not specify names, they will be called "output_hitting" and "output_pitching", respectively.

### Example Usage
- To access the help at any time, enter "python main.py --help-me"
- The general structure of the command is "python main.py <your_copied_url> --hit <name> --pitch name"
- A concrete example of the command is "python main.py https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats --hit UConn_hit1 --pitch UConn_pitch1"