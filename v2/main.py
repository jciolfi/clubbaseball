from gc_auto import *
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Must specify stats link to pull from. For example:')
        print(f'  python gc_auto.py "https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats?start_ts=1682866800&end_ts=1682866800"')
        sys.exit(0)

    gc_init()

    with requests.Session() as session:
        # csrfmiddlewaretoken = GET_login(session)
        # print(csrfmiddlewaretoken)
        # POST_login(session, csrfmiddlewaretoken)
        # POST_logout(session, csrfmiddlewaretoken)
        hitting_stats, pitching_stats = GET_stats(session, sys.argv[1])
        write_hitting_stats(hitting_stats)
        write_pitching_stats(pitching_stats)