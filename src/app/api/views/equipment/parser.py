from flask_restful import reqparse

def build_equipment_parser():
  parser = reqparse.RequestParser()
  parser.add_argument('tag', type=str, required=True)
  parser.add_argument('brand', type=str)
  parser.add_argument('model', type=str)
  parser.add_argument('series', type=str)

  return parser

def build_equipment_update_parser():
  parser = reqparse.RequestParser()
  parser.add_argument('tag', type=str)
  parser.add_argument('brand', type=str)
  parser.add_argument('model', type=str)
  parser.add_argument('series', type=str)

  return parser