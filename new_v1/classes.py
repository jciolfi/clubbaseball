from dataclasses import dataclass

# dataclass for NCBA-ordered offensive stats
# note: IBB is not stored in GameChanger Classic
@dataclass
class Offsense:
    ab: str = 'N/A'
    r: str = 'N/A'
    h: str = 'N/A'
    doubles: str = 'N/A'
    triples: str = 'N/A'
    hr: str = 'N/A'
    rbi: str = 'N/A'
    bb: str = 'N/A'
    ibb: str = 'N/A'
    so: str = 'N/A'
    sb: str = 'N/A'
    cs: str = 'N/A'
    sac_f: str = 'N/A'
    sac_b: str = 'N/A'
    hbp: str = 'N/A'


# dataclass for the NCBA-ordered pitching stats
# note: cg & sho are not stored in GameChanger Classic
@dataclass
class Pitching:
    started: str = 'N/A'
    w: str = 'N/A'
    l: str = 'N/A'
    cg: str = 'N/A'
    sho: str = 'N/A'
    sv: str = 'N/A'
    svo: str = 'N/A'
    ip: str = ''
    h: str = 'N/A'
    r: str = 'N/A'
    er: str = 'N/A'
    hr: str = 'N/A'
    hbp: str = 'N/A'
    bb: str = 'N/A'
    ibb: str = 'N/A'
    so: str = 'N/A'
    bk: str = 'N/A'
    wp: str = 'N/A'
    pk: str = 'N/A'