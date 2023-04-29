"""felhasználók kezelése"""
from .dataStruct import User

class UsersManage():
    "Regisztrált felhasználók kezelése"
    def __init__(self, users = []) -> None:
        self._users:list[User] = []
        self._init_users(users) # userek betevése az User osztályba
        # ezeknek van dcid, username, password, eloadasShow

    def _init_users(self,users) -> None:
        """"Userek initelése az User classba"""
        for user in users:
            if isinstance(user, User): # ha már egy usert kaptunk
                self._users.append(user)
            else:
                new_user = User(user)
                self._users.append(new_user)

    def get_user(self, dcid) -> User | None:
        "DCid alapján vissza adja az users, HA van regisztrálva"
        for user in self._users:
            if user.dcid == str(dcid):
                return user
        return None

    def get_all_user(self) -> list[User]:
        "Vissza adja az összes Userst"
        return self._users

    def set_user(self, users):
        "Összes user beállítása"
        self._init_users(users)

    def remove_user(self, dcid):
        "Kitörli a felhasználót user id alapján"
        new_users = []
        for user in self._users:
            if user.dcid != str(dcid):
                new_users.append(user)
        self._users = new_users

    def add_user(self,user):
        "Új user regisztrálása user: List[dict]"
        self._init_users(user)
