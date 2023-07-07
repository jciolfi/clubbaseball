# clubbaseball

## Motivation
The National Club Baseball Association (NCBA) allows teams to self-report their statistics and upload them onto their website. Stats are uploaded per-player in a particular order one-by-one:

<style>
    .image-container {
        display: flex;
        flex-wrap: wrap;
        margin-right: -10px;
        justify-content: center;
    }
    .image-container img {
        width: 45%;
        margin-right: 10px;
        margin-bottom: 10px;
    }
</style>

<div class="image-container">
    <img src="media/entering%20stats/NCBA/NCBA%20hitting.png" alt="Image 1" />
    <img src="media/entering%20stats/NCBA/NCBA%20pitching.png" alt="Image 2" />
</div>

In GameChanger, the most popular digital option for recording baseball game statistics, the information required to enter statistics into the NCBA spans across separate, disparate tables. 

In the NCBA website, all statistics that weren't submitted are cleared when the currently selected player is switched. This means that filling out each player requires switching across 3+ tables on the GameChanger website, which is extremely inefficient and tedious.

This code aims to automate the process of collecting statistics by pulling data from relevant tables in GameChanger and outputting the statistics in the order expected by the NCBA.

## Demo
See the following [video](https://youtu.be/wzqZL1Tiu7w) for a demo on the setup and execution for the stats scraper. Fast forward to 0:45 to skip the setup and just see a demo.

## v2
This is a more automated option. It will log in for you and output the same information with you doing less work. All you need to do is the setup, and then you are good to go.

### .env
1. `touch v2/.env`
2. Open the file `v2/.env` in any text editor and paste the following into it. Fill in the email and password you use to log into GameChanger:

```
email=
password=
```


**Note:** that you must be admin (or have GameChanger premium) to access the stats.

### Instructions to Execute the Program
1. Navigate to GameChanger Classic. Log in and select the "Season Stats" tab. Select the appropriate date range
2. Copy the URL in the top bar.
3. Execute "./run \<your_copied_url\>".
4. If you would like to name the output spreadsheets, you can do so by appending "--hit \<name\>" and "--pitch \<name\>"'. If you do not specify names, they will be called "hit_stats" and "pitch_stats", respectively.

### Example Usage
- To access the help at any time, enter "./run --help-me"
- The general structure of the command is "./run \<your_copied_url\> --hit \<name\> --pitch \<name\>"
- A concrete example of the command is "./run https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats --hit UConn_hit1 --pitch UConn_pitch1"


## v1 (Deprecated)
Need to copy/paste stats tables from "Season Stats" tab into the corresponding variables. Must log in on your own in a browser, navigate to the tab, and select the stat range (typically one game at a time) for 
- Hitting stat tables: "Standard", "Patience, Speed & Power", "QABs & Team Impact"
- Pitching stat tables: "Standard", "Command", "Batter Results", "Runs & Running Game"