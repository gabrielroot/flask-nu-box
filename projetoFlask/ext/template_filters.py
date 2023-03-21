import locale
import pytz

def init_app(app):
    @app.template_filter()
    def format_datetime(value, formatTo, tz=app.config.TIMEZONE):
        value = value.replace(tzinfo=pytz.utc)
        return value.astimezone(pytz.timezone(tz)).strftime(formatTo)

    @app.template_filter()
    def format_money(value, toLocale=app.config.LOCALE):
        locale.setlocale(locale.LC_ALL, toLocale)
        return locale.currency(value)