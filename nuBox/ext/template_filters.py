import locale

import pytz


def init_app(app):
    @app.template_filter()
    def format_datetime(date_time, formatTo, tz=app.config.TIMEZONE):
        date_time = date_time.replace(tzinfo=pytz.utc)
        return date_time.astimezone(pytz.timezone(tz)).strftime(formatTo)

    @app.template_filter()
    def format_money(value, toLocale=app.config.LOCALE):
        locale.setlocale(locale.LC_ALL, toLocale)
        return locale.currency(value if value else 0)
