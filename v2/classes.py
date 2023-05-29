from dataclasses import dataclass

# dataclass for NCBA-ordered offensive stats
# note: IBB is not stored in GameChanger Classic
@dataclass
class Hitting:
    ab: int = 0
    r: int = 0
    h: int = 0
    doubles: int = 0
    triples: int = 0
    hr: int = 0
    rbi: int = 0
    bb: int = 0
    ibb: int = 0
    so: int = 0
    sb: int = 0
    cs: int = 0
    sac_f: int = 0
    sac_b: int = 0
    hbp: int = 0


# dataclass for the NCBA-ordered pitching stats
# note: cg & sho are not stored in GameChanger Classic
@dataclass
class Pitching:
    started: int = 0
    w: int = 0
    l: int = 0
    cg: str = 'N/A'
    sho: str = 'N/A'
    sv: int = 0
    svo: int = 0
    ip: str = ''
    h: int = 0
    r: int = 0
    er: int = 0
    hr: int = 0
    hbp: int = 0
    bb: int = 0
    ibb: int = 0
    so: int = 0
    bk: int = 0
    wp: int = 0
    pk: int = 0