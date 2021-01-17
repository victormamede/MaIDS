from flask_restful import reqparse


def build_equipment_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tag', type=str, required=True)
    parser.add_argument('type_id', type=int, required=True)
    parser.add_argument('brand', type=str)
    parser.add_argument('model', type=str)
    parser.add_argument('series', type=str)

    return parser


def build_equipment_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tag', type=str)
    parser.add_argument('type_id', type=int)
    parser.add_argument('brand', type=str)
    parser.add_argument('model', type=str)
    parser.add_argument('series', type=str)

    return parser


def build_equipment_filter_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('tag', type=str, location='args')
    parser.add_argument('type_id', type=int, location='args')
    parser.add_argument('brand', type=str, location='args')
    parser.add_argument('model', type=str, location='args')
    parser.add_argument('series', type=str, location='args')

    return parser
