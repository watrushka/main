from dataclasses import dataclass
from datetime import date


def date_from_str(dob_text):
    if dob_text == None:
        return date(1, 1, 1)
    dob = [int(i) for i in dob_text.split(".")]
    return date(dob[2], dob[1], dob[0])


@dataclass()
class Employee:
    id: int
    fullname: str
    dob: date
    groupid: int
    positionid: int
    picture: str

    def __init__(self, id, fullname, dob, groupid, posistionid, picture):
        self.id = id
        self.fullname = fullname
        self.dob = date_from_str(dob)
        self.groupid = groupid
        self.positionid = posistionid
        self.picture = picture

    def to_dict(self):
        return {
            "Fullname": self.fullname,
            "DOB": self.dob.strftime("%d.%m.%Y"),
            "GroupId": self.groupid,
            "PositionId": self.positionid,
            "Picture": self.picture
        }


@dataclass()
class Group:
    id: int
    title: str
    departmentid: int

    def to_dict(self):
        return {
            "Title": self.title,
            "DepartmentId": self.departmentid,
        }


@dataclass()
class Department:
    id: int
    title: str

    def to_dict(self):
        return {
            "Title": self.title,
        }


@dataclass()
class Position:
    id: int
    title: str

    def to_dict(self):
        return {
            "Title": self.title,
        }
