from flask_restful import reqparse


def build_type_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("description", type=str, required=True)

    return parser


def build_type_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("description", type=str)

    return parser
