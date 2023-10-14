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

        player_name = f"{row[1]}, {row[2]}"
        
        # player got > 0 PAs
        if int(row[4]) > 0:
            # AB, R, H, 2B, 3B, HR, RBI, BB, IBB, SO, SB, CS, SAC-F, SAC-B, HBP
            offensive_stats[player_name] = Offsense(row[5], row[16], row[10], row[12], row[13], row[14], row[15], row[17], 'N/A', row[18], row[25], row[27], row[21], row[22], row[20])

        # player threw more than 0 pitches
        if int(row[58]) > 0:
            # started, W, L, CG, SHO, SV, SVO, IP, H, R, ER, HR, HBP, BB, IBB, SO, BK, WP, PK
            pitching_stats[player_name] = Pitching(row[56], row[59], row[60], '0', '0', row[61], row[62], row[54], row[65], row[66], row[67], row[106], row[71], row[68], 'N/A', row[69], row[75], row[80], row[76])

    if len(pitching_stats) == 1:
        for pitcher in pitching_stats:
            pitcher_stats = pitching_stats[pitcher]
            pitcher_stats.cg = '1'
            pitcher_stats.sho = '1' if pitcher_stats.r == '0' else '0'


def export_stats(filename):
    if not filename:
        filename = "gc_stats.csv"
    else:
        filename += ".csv"
    
    with open(f"{filename}", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["OFFENSIVE STATS"])
        writer.writerow(["Name", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "SB", "CS", "SAC_F", "SAC_B", "HBP"])

        hitters = sorted(list(offensive_stats.keys()))
        for hitter in hitters:
            stats = offensive_stats[hitter]
            writer.writerow([hitter,
                             stats.ab, 
                             stats.r, 
                             stats.h, 
                             stats.doubles, 
                             stats.triples, 
                             stats.hr, 
                             stats.rbi, 
                             stats.bb,
                             stats.ibb,
                             stats.so,
                             stats.sb,
                             stats.cs,
                             stats.sac_f,
                             stats.sac_b,
                             stats.hbp])
            
        writer.writerow([])
        writer.writerow(["PTICHING STATS"])
        writer.writerow(["Name", "Started", "W", "L", "CG", "SHO", "SV", "SVO", "IP", "H", "R", "ER", "HR", "HBP", "BB", "IBB", "SO", "BK", "WP", "PK"])
        pitchers = sorted(list(pitching_stats.keys()))
        for pitcher in pitchers:
            stats = pitching_stats[pitcher]
            writer.writerow([pitcher,
                             stats.started,
                             stats.w,
                             stats.l,
                             stats.cg,
                             stats.sho,
                             stats.sv,
                             stats.svo, 
                             stats.ip,
                             stats.h,
                             stats.r, 
                             stats.er, 
                             stats.hr, 
                             stats.hbp, 
                             stats.bb, 
                             stats.ibb, 
                             stats.so, 
                             stats.bk, 
                             stats.wp, 
                             stats.pk])


if __name__ == "__main__":
    argc = len(sys.argv)
    if not (3 <= argc <= 4):
        print("Usage: ./run [path_to_exported_stats.csv]")
        print("Usage: ./run [path_to_exported_stats.csv] [output_filename]")
        exit(1)

    stats_path = sys.argv[2]
    output_filename = sys.argv[3] if argc == 4 else "gc_stats"
    fp = None
    try:
        fp = open(stats_path)
    except:
        print(f"Could not find path to file: {stats_path}")
        exit(1)

    print("Parsing...")
    parse_stats(fp)
    fp.close()
    export_stats(output_filename)
    print(f"\nExported stats to {output_filename}.csv")