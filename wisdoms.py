WISDOMS = [
    "birdsong", "preservation", "bosk",
    "skolekosophy", "nyctodromy", "hushery",
    "illumination", "ithastry", "horomachistry"
]

def comma_seperated_wisdoms():
    '''Return a comma seperated list of wisdoms for SQLite commands'''
    return ',' + ','.join(WISDOMS)

def colon_seperated_wisdoms():
    '''Return a comma and colon seperated list of wisdoms for executemany()'''
    return ',:' + ',:'.join(WISDOMS)

def comma_seperated_evolve_wisdoms():
    '''Return a comma seperated list of wisdoms for SQLite commands'''
    return ',e_' + ',e_'.join(WISDOMS)

def colon_seperated_evolve_wisdoms():
    '''Return a comma and colon seperated list of wisdoms for executemany()'''
    return ',:e_' + ',:e_'.join(WISDOMS)
