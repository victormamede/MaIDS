from flask_restful import reqparse

def construct_auth_parser():
  parser = reqparse.RequestParser()
  parser.add_argument('username', type=str, required=True)
  parser.add_argument('password', type=str, required=True)

  return parser