from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_user, name, lastname, address, phone, dateBirth, role, image, username, password):
        self.id_user = id_user
        self.name = name
        self.lastName = lastname
        self.address = address
        self.phone = phone
        self.dateBirth = dateBirth
        self.role = role
        self.image = image
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active