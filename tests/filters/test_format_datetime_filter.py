from datetime import datetime


def test_should_format_date(app):
    assert 'format_datetime' in app.jinja_env.filters

    my_datetime = datetime(2002, 2, 2, 15, 45)
    assert app.jinja_env.\
        filters['format_datetime'](my_datetime,
                                   '%d/%m/%Y') == '02/02/2002'
