from .roles import Role

def encode_roles(*roles):
  used_roles = set()
  encoded = 0

  for raw_role in roles:
    try:
      role = Role[raw_role]
    except KeyError:
      continue

    if(role in used_roles):
      continue

    used_roles.add(role)
    encoded += pow(2, role.value)

  return encoded

def decode_roles(encoded):
  current = encoded
  index = 0
  roles = set()

  while current > 0:
    if current % 2 == 1:
      roles.add(Role(index))
      current -= 1
    
    current /= 2
    index += 1

  return roles
