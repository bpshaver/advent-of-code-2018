from inspector import Inspector

bulletin1 = """Deny citizens of Russia
               Allow citizens of Belarus
               """

entrant1 = {
    "passport": """ID#: GC07D-FU8AR
    NATION: Arstotzka
    NAME: Guyovich, Russian
    DOB: 1933.11.28
    SEX: M
    ISS: East Grestin
    EXP: 1983.07.10"""
}

def test_str_to_dict():
    inspector = Inspector()
    assert inspector._str_to_dict(entrant1['passport']) == {
        'ID#': 'GC07D-FU8AR',
        'NATION': 'Arstotzka',
        'NAME': 'Guyovich, Russian',
        'DOB': '1933.11.28',
        'SEX': 'M',
        'ISS': 'East Grestin',
        'EXP': '1983.07.10'
        }

def test_parse_bulletin():
    inspector = Inspector()
    assert inspector._parse_bulletin(bulletin1) == [
        'Deny citizens of Russia', 'Allow citizens of Belarus'
        ]

def test_denied_citizens():
    inspector = Inspector()
    inspector.receive_bulletin(bulletin1)
    assert inspector.inspect({'passport':'NATION: Russia'}).startswith('Entry denied')

def test_russia_denied_country():
    inspector = Inspector()
    inspector.receive_bulletin(bulletin1)
    assert 'Russia' in inspector.state_dict['denied_countries']

def test_allowed_denied_countries_updated():
    inspector = Inspector()
    inspector.receive_bulletin(bulletin1)
    assert inspector.state_dict['denied_countries'] == ['Russia']
    assert inspector.state_dict['allowed_countries'] == ['Belarus']
    inspector.receive_bulletin("""Deny citizens of Belarus
                                Allow citizens of Albania""")
    assert inspector.state_dict['denied_countries'] == ['Russia', 'Belarus']
    assert inspector.state_dict['allowed_countries'] == ['Albania']

def test_expired_passport_denied():
    inspector = Inspector()
    assert inspector.inspect({'passport':'EXP: 1981.12.01'}) == 'Entry denied: passport expired'
    assert inspector.inspect({'passport':'EXP: 1982.11.22'}) == 'Entry denied: passport expired'

# bulletin1 = """Deny citizens of Russia
#                Allow citizens of Belarus
