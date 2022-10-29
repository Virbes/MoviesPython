from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_user, name, last_name, address, phone, date_birth, role, image, username, password):
        self.id_user = id_user
        self.name = name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.date_birth = date_birth
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
