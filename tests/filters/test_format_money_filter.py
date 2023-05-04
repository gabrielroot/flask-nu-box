def test_should_format_to_BRL(app):
    assert 'format_money' in app.jinja_env.filters
    assert app.jinja_env.\
        filters['format_money'](10) == 'R$ 10,00'
