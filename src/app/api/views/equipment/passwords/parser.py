from flask_restful import reqparse


def build_user_password_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("user_id", type=int, required=True)
    parser.add_argument("username", type=str, required=True)
    parser.add_argument("password", type=str, required=True)

    return parser


def build_level_password_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("level", type=str, required=True)
    parser.add_argument("username", type=str, required=True)
    parser.add_argument("password", type=str, required=True)

    return parser
