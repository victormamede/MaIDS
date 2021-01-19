from flask_restful import reqparse


def build_auth_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    return parser


def build_password_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True)

    return parser
