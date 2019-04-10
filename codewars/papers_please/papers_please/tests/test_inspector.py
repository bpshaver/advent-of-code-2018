from inspector import Inspector

bulletin1 = """Deny citizens of Russia
               Allow citizens of Belarus
               """

def test_denied_citizens():
    inspector = Inspector()
    inspector.receive_bulletin(bulletin1)
    assert inspector.inspect({'passport':'NATION: Russia'}).startswith('Denied')

def test_russia_denied_country():
    inspector = Inspector()
    inspector.receive_bulletin(bulletin1)
    assert 'Russia' in inspector.state_dict['denied_countries']