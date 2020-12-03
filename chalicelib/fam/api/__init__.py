from .account import account_blueprint
from .query import query_blueprint
from .root import root_blueprint


def apply_routes(chalice_app):
    pass
    chalice_app.register_blueprint(account_blueprint)
    chalice_app.register_blueprint(query_blueprint)
    chalice_app.register_blueprint(root_blueprint)
