import sqlite3
from typing import List, Tuple
from models import Employee, Group, Department, Position


def get_param_as_string(param):
    return f"{param}" if param.isdigit() else f"'{param}'"


class EmployeesDBService:
    employees = "employees"
    departments = "departments"
    groups = "groups"
    positions = "positions"

    _type_to_table = {
        Department: departments,
        Group: groups,
        Employee: employees,
        Position: positions
    }

    def __init__(self):
        self._connection = sqlite3.connect("personnel_management_system.db")

    # private methods

    def _execute_and_commit(self, query):
        self._connection.cursor().execute(query)
        self._connection.commit()

    def _get_query_result(self, query):
        return self._connection.cursor().execute(query).fetchall()

    def _get_all(self, table, field):
        return self._get_query_result(f"""SELECT {field} FROM {table}""")

    def _get_all_where(self, table, field, filter_field, filter_field_value):
        return self._get_query_result(
            f"""SELECT {field} FROM {table} WHERE {filter_field} = {get_param_as_string(str(filter_field_value))}""")

    def _delete(self, table, id):
        self._execute_and_commit(f"""DELETE FROM {table} WHERE id = {id}""")

    def _add(self, table, **kwargs):
        fields = list(kwargs.keys())
        params = [get_param_as_string(str(kwargs[k])) for k in fields]
        self._execute_and_commit(f"""INSERT INTO {table}({", ".join(fields)}) VALUES({', '.join(params)})""")

    def _update(self, table, id, **kwargs):
        params = [f"""{k} = {get_param_as_string(str(v))}""" for k, v in kwargs.items()]
        self._execute_and_commit(f"""UPDATE {table} SET {', '.join(params)} WHERE id = {id}""")

    def _get_all_employees_sorted(self, value, increase):
        return f"""SELECT employees.id, employees.Fullname, employees.DOB, groups.Title, positions.Title, 
employees.picture 
                    FROM employees LEFT JOIN groups ON employees.GroupId = groups.id 
                    LEFT JOIN positions ON employees.PositionId = positions.id ORDER BY employees.{value} {increase}"""

    def _get_all_groups_sorted(self, value, increase):
        return f"""SELECT groups.id, groups.Title, departments.Title 
        FROM groups LEFT JOIN departments ON groups.DepartmentId = departments.id ORDER BY groups.{value} {increase}"""

    def _get_all_deppos_sorted(self, table, value, increase):
        return f"""SELECT * FROM {table} ORDER BY {table}.{value} {increase}"""

    def _sort(self, table, value, increase):
        if table == EmployeesDBService().employees:
            if value == "Id":
                if increase == "По возрастанию":
                    return self._get_all_employees_sorted("id", "ASC")
                else:
                    return self._get_all_employees_sorted("id", "DESC")
            elif value == "Возрасту":
                if increase == "По возрастанию":
                    return self._get_all_employees_sorted("DOB", "DESC")
                else:
                    return self._get_all_employees_sorted("DOB", "ASC")
            else:
                if increase == "По возрастанию":
                    return self._get_all_employees_sorted("Fullname", "DESC")
                else:
                    return self._get_all_employees_sorted("Fullname", "ASC")
        elif table == EmployeesDBService().groups:
            if value == "Id":
                if increase == "По возрастанию":
                    return self._get_all_groups_sorted("id", "ASC")
                else:
                    return self._get_all_groups_sorted("id", "DESC")
            else:
                if increase == "По возрастанию":
                    return self._get_all_groups_sorted("Title", "DESC")
                else:
                    return self._get_all_groups_sorted("Title", "ASC")
        else:
            if value == "Id":
                if increase == "По возрастанию":
                    return self._get_all_deppos_sorted(table, "id", "ASC")
                else:
                    return self._get_all_deppos_sorted(table, "id", "DESC")
            else:
                if increase == "По возрастанию":
                    return self._get_all_deppos_sorted(table, "Title", "DESC")
                else:
                    return self._get_all_deppos_sorted(table, "Title", "ASC")



    # public methods

    def close(self):
        self._connection.close()

    def get_employees_for_display(self) -> List[Tuple]:
        query = """SELECT employees.id, employees.Fullname, employees.DOB, groups.Title, positions.Title 
        FROM employees LEFT JOIN groups ON employees.GroupId = groups.id 
        LEFT JOIN positions ON employees.PositionId = positions.id;"""
        return self._get_query_result(query)

    def get_groups_for_display(self) -> List[Tuple]:
        query = """SELECT groups.id, groups.Title, departments.Title 
        FROM groups LEFT JOIN departments ON groups.DepartmentId = departments.id;"""
        return self._get_query_result(query)

    def get_departments_for_display(self) -> List[Tuple]:
        return self._get_all(EmployeesDBService.departments, "*")

    def get_positions_for_display(self) -> List[Tuple]:
        return self._get_all(EmployeesDBService.positions, "*")

    def get_employees(self) -> List[Employee]:
        return [Employee(*v) for v in self._get_all(EmployeesDBService.employees, "*")]

    def get_groups(self) -> List[Group]:
        return [Group(*v) for v in self._get_all(EmployeesDBService.groups, "*")]

    def get_departments(self) -> List[Department]:
        return [Department(*v) for v in self._get_all(EmployeesDBService.departments, "*")]

    def get_positions(self) -> List[Position]:
        return [Position(*v) for v in self._get_all(EmployeesDBService.positions, "*")]

    def get_employee(self, id) -> Employee:
        t = self._get_all_where(EmployeesDBService.employees, '*', 'id', id)[0]
        return Employee(*t)

    def get_group(self, id) -> Group:
        t = self._get_all_where(EmployeesDBService.groups, '*', 'id', id)[0]
        return Group(*t)

    def get_department(self, id) -> Department:
        t = self._get_all_where(EmployeesDBService.departments, '*', 'id', id)[0]
        return Department(*t)

    def get_position(self, id) -> Position:
        t = self._get_all_where(EmployeesDBService.positions, '*', 'id', id)[0]
        return Position(*t)

    def delete_item(self, item):
        self._delete(EmployeesDBService._type_to_table[type(item)], item.id)

    def add_item(self, item):
        self._add(EmployeesDBService._type_to_table[type(item)], **item.to_dict())

    def update_item(self, item):
        self._update(EmployeesDBService._type_to_table[type(item)], item.id, **item.to_dict())

    def sort_item(self, table, value, increase):
        return self._get_query_result(self._sort(table, value, increase))

