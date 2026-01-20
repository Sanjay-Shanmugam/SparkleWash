from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, role, phone=None, vehicle_no=None, vehicle_type=None):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.phone = phone
        self.vehicle_no = vehicle_no
        self.vehicle_type = vehicle_type
