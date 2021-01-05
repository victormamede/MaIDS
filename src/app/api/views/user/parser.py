from flask_restful import reqparse
from ....util.auth import Role


def build_user_creation_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('real_name', type=str, required=True)
    parser.add_argument('registration_number', type=int, required=True)
    parser.add_argument('roles',
                        type=str,
                        action='append',
                        required=True,
                        choices=[*[role.name for role in list(Role)], 'NONE'])
    parser.add_argument('email', type=str, required=True)

    return parser


def build_user_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('real_name', type=str)
    parser.add_argument('registration_number', type=int)
    parser.add_argument('roles',
                        type=str,
                        action='append',
                        choices=[*[role.name for role in list(Role)], 'NONE'])
    parser.add_argument('email', type=str)

    return parser


def build_user_filter_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, location='args')
    parser.add_argument('real_name', type=str, location='args')
    parser.add_argument('registration_number', type=str, location='args')
    parser.add_argument('email', type=str, location='args')

    return parser
