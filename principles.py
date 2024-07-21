
PRINCIPLES = [
    "edge", "forge", "grail", "heart", "knock", "lantern",
    "moon", "moth", "nectar", "rose", "scale", "sky", "winter"
]

def comma_seperated_principles():
    '''Return a comma seperated list of principles for SQLite commands'''
    return ',' + ','.join(PRINCIPLES)

def colon_seperated_principles():
    '''Return a comma and colon seperated list of principles for executemany()'''
    return ',:' + ',:'.join(PRINCIPLES)
