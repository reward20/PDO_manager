from sqlalchemy import delete, select

from yz_pdo.src.models import Profiles
from .db_connect import DbConnect


__all__ = [
    "ProfilesView",
    "ProfilesWriter",
]


class ProfileExist(DbConnect):

    def exist_profile(self, profile_name: str) -> Profiles | None:

        exist_sub = (
            select(Profiles).
            where(Profiles.name == profile_name).
            exists()
        )

        stmt_exist = (
            select(Profiles).
            where(exist_sub).
            where(Profiles.name == profile_name)
        )

        result = self.session.scalar(stmt_exist)
        return result


class ProfilesCreate(ProfileExist):

    def add_profile(self, profiles_name: str) -> Profiles:
        result = self.exist_profile(profiles_name)
        if result is not None:
            return result
        new_line = Profiles(name=profiles_name)
        self.session.add(new_line)
        return new_line


class ProfilesDelete(ProfileExist):

    def delete_profile(self, profiles_name: str) -> None:
        if self.exist_profile(profiles_name) is None:
            raise ValueError(f"Profiles '{profiles_name} 'is not found in table '{Profiles.__tablename__}'")
        else:
            stmt_delete = (
                delete(Profiles).
                where(Profiles.name == profiles_name)
            )
            self.session.execute(stmt_delete)


class ProfilesView(ProfileExist):

    def get_profile(self, profiles_name) -> Profiles:
        result = self.exist_profile(profiles_name)
        if result is None:
            raise ValueError(f"Profile '{profiles_name}' is not found in table '{Profiles.__tablename__}'")
        return result


class ProfilesWriter(ProfilesCreate, ProfilesDelete):
    pass
