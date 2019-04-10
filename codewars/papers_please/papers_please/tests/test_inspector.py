from inspector import Inspector

bulletin1 = """Deny citizens of Russia
               Allow citizens of Belarus
               """

def test_denied_citizens_denied():
    inspector = Inspector()
    Inspector.receive_bulletin(bulletin1)
    assert inspector.inspect({'passport':'NATION: Russia'}).startswith('Denied')