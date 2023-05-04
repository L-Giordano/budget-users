class UserError(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje


class PasswordError(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
