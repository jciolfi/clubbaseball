from gc_auto import *
import requests, argparse, sys

# Print helpful usage message when --help-me is invoked
def print_help():
    print('This is a web scraper to export stats from GameChanger to a spreadsheet in the order the NCBA expects it.')
    print('\nINSTRUCTIONS:')
    print('   0. Read README.md, make sure your .env is set up')
    print('   1. Navigate to GameChanger Classic. Log in and select the "Season Stats" tab. Select the appropriate date range')
    print('   2. Copy the URL in the top bar')
    print('   3. Type "python main.py <your_copied_url>')
    print('   4. If you would like to name the output spreadsheets, you can do so by appending "--hit <name>" and "--pitch <name>"')
    print('      If you do not specify names, they will be called output_hitting and output_pitching, respectively')
    print('\nEXAMPLE USAGE:')
    print('   "python main.py <your_copied_url> --hit <name> --pitch name"')
    print('   "python main.py https://gc.com/t/spring-2023/northeastern-university-huskies-club-640424614cea87ae8c000001/stats --hit UConn_hit1 --pitch UConn_pitch1"')


if __name__ == "__main__":
    # initialize command line args
    gc_url = None
    hitting_name = None
    pitching_name = None

    # add command line arguments and help
    parser = argparse.ArgumentParser(description='Process a URL.')
    parser.add_argument('gamechanger_url', nargs='?', help='The GameChanger Season Stats URL to process')
    parser.add_argument('--help-me', action='store_true', help='Display help message')
    parser.add_argument('--hit', nargs='?', const='', help='Specify the filename for the hitting stats, e.g. UConn_hitting1')
    parser.add_argument('--pitch', '--filename_p', nargs='?', const='', help='Specify the filename for the pitching stats, e.g. UConn_pitching1')

    # check if --help-me is inputted
    args = parser.parse_args()
    if args.help_me:
        print_help()
        sys.exit(0)
        
    # validate url is a GameChanger URL
    gc_url = args.gamechanger_url
    if not gc_url or not gc_url.startswith('https://gc.com/'):
        print('Please input a GameChanger URL.')
        print('If you need help, enter "python main.py --help-me"')
        sys.exit(1)
    
    # set output csv names, if applicable
    if args.hit == args.pitch:
        print('The hitting and pitching files cannot have the same name.')
        sys.exit(1)
    if args.hit:
        hitting_name = args.hit
    if args.pitch:
        pitching_name = args.pitch

    # initialize session cookies, env variables
    gc_init()

    with requests.Session() as session:
        # log in and get csrfmiddlewaretoken for authentication
        TEST_john()
        
        # scrape the hitting and pitching stats, export them to respective csv's
        hitting_stats, pitching_stats = GET_stats(session, gc_url)
        write_hitting_stats(f'{hitting_name}.csv', hitting_stats)
        write_pitching_stats(f'{pitching_name}.csv', pitching_stats)
        POST_logout(session)