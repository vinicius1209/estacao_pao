from .models import Usuario

def authenticate(username, password):
    user = Usuario.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return Usuario.query.get(user_id)