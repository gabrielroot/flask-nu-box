from flask import Blueprint

from .views import authView

bpAuth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    url_prefix="/auth"
)

bpAuth.add_url_rule('/login', view_func=authView.login)
bpAuth.add_url_rule('/login', view_func=authView.login_post, methods=['POST'])
bpAuth.add_url_rule('/signup', view_func=authView.signup)
bpAuth.add_url_rule('/signup', view_func=authView.signup_post,
                    methods=['POST']
                    )
bpAuth.add_url_rule('/logout', view_func=authView.logout)
