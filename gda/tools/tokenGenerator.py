import uuid


# This is a very simple funcition that generates an uuid
# and then generats a sha1 hash using the uuid and the name passded to it
# any good ideias would be great
# i know that sha1 is not the most secure hash function, but if banks use it...
def generateToken(name):
    identifier = uuid.uuid4()
    return uuid.uuid5(identifier, str(name)).hex
