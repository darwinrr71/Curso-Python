Suma flexible

def add_all(*args):
    return sum(args)


Crear perfil flexible

def create_profile(name, **extra_data):
    profile = {"name": name, **extra_data}
    return profile
