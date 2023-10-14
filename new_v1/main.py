import sys, csv
from classes import Offsense, Pitching

offensive_stats = {}
pitching_stats = {}

def parse_stats(fp):
    reader = csv.reader(fp)
    # skip over header and column titles
    next(reader)
    next(reader)
    global hitting_stats, pitching_stats
    for row in reader:
        try:
            # first row should be player number
            int(row[0])
        except:
            break

        # if they didn't play in this game
        if int(row[3]) == 0:
            continue

        player_name = f"{row[1]}, {row[2]}"
        
        # player got > 0 PAs
        if int(row[4]) > 0:
            # AB, R, H, 2B, 3B, HR, RBI, BB, IBB, SO, SB, CS, SAC-F, SAC-B, HBP
            offensive_stats[player_name] = Offsense(row[5], row[16], row[10], row[12], row[13], row[14], row[15], row[17], 'N/A', row[18], row[25], row[27], row[21], row[22], row[20])

        # player has more than 0 IPs
        if row[54] != "0.0":
            # started, W, L, CG, SHO, SV, SVO, IP, H, R, ER, HR, HBP, BB, IBB, SO, BK, WP, PK
            player_pitching = Pitching(row[56], row[59], row[60], '0', '0', row[61], row[62], row[54], row[65], row[66], row[67], row[106], row[71], row[68], 'N/A', row[69], row[75], row[80], row[76])

    if len(pitching_stats) == 1:
        for pitcher in pitching_stats:
            pitcher_stats = pitching_stats[pitcher]
            pitcher_stats.cg = '1'
            pitcher_stats.sho = '1' if pitcher_stats.r == '0' else '0'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./run [path_to_exported_stats.csv]")
        exit(1)

    stats_path = sys.argv[1]
    fp = None
    try:
        fp = open(stats_path)
    except:
        print(f"Could not find path to file: {stats_path}")
        exit(1)

    parse_stats(fp)
    fp.close()