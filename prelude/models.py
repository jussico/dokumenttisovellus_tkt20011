
class User:
    def __init__(self, username, first_name, last_name, password, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def idenfitier_string(self):
        return f"{self.username} {self.first_name} {self.last.name} Admin: {self.is_admin}"

    def __str__(self):
        return self.username + " "\
            + self.first_name + " "\
            + self.last_name + " "\
            + self.password + " "\
            + str(self.is_admin)
