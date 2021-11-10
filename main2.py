import sys

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QFileDialog, QMessageBox, QTableWidget

from employeedbservice import *

import enum


class WindowMode(enum.Enum):
    insert = 0
    update = 1


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.dbservice = EmployeesDBService()

        uic.loadUi('pr.ui', self)
        self.buttons_connections()
        self.table_employees = QTableWidget()


        self.table_groups = QTableWidget()
        self.table_departments = QTableWidget()
        self.table_positions = QTableWidget()
        self.insert_data_in_table(self.dbservice.get_employees_for_display(), self.table_employees, 5,
                                  ["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])
        self.insert_data_in_table(self.dbservice.get_groups_for_display(), self.table_groups, 3,
                                  ["ИД", "Группа", "Отдел"])
        self.insert_data_in_table(self.dbservice.get_departments_for_display(), self.table_departments, 2, ["ИД", "Отдел"])
        self.insert_data_in_table(self.dbservice.get_positions_for_display(), self.table_positions, 2, ["ИД", "Должность"])
        self.select_data()

    def buttons_connections(self):
        self.addemployee.clicked.connect(self.add)
        self.editemployee.clicked.connect(self.edit_employees)
        self.deleteemployee.clicked.connect(self.delete_employee)
        self.addgroup.clicked.connect(self.add)
        self.editgroup.clicked.connect(self.edit_groups)
        self.deletegroup.clicked.connect(self.delete_group)
        self.adddep.clicked.connect(self.add)
        self.editdep.clicked.connect(self.edit_departments)
        self.deletedep.clicked.connect(self.delete_department)
        self.addpos.clicked.connect(self.add)
        self.editpos.clicked.connect(self.edit_positions)
        self.deletepos.clicked.connect(self.delete_position)
        self.tableWidget.itemClicked.connect(self.set_photo)
        self.search_line.textChanged.connect(self.find_employee)
        self.sort1_emp.currentTextChanged.connect(self.sorting_emp)
        self.sort2_emp.currentTextChanged.connect(self.sorting_emp)
        self.sort1_gr.currentTextChanged.connect(self.sorting_gr)
        self.sort2_gr.currentTextChanged.connect(self.sorting_gr)
        self.sort1_dep.currentTextChanged.connect(self.sorting_dep)
        self.sort2_dep.currentTextChanged.connect(self.sorting_dep)
        self.sort1_pos.currentTextChanged.connect(self.sorting_pos)
        self.sort2_pos.currentTextChanged.connect(self.sorting_pos)

    def get_id_by_row(self, table):
        ID = False
        row = table.currentRow()
        if row >= 0:
            fl = table.item(row, 0).text()
            ID = int(fl)
        return ID

    def set_photo(self):
        image_path = self.dbservice.get_employee(window.get_id_by_row(window.tableWidget)).picture
        pixmap = QPixmap(f'{image_path}')
        pixmap = pixmap.scaled(350, 450)
        self.picture.setPixmap(pixmap)

    def select_data(self):
        self.insert_data_in_table(self.dbservice.get_employees_for_display(), self.tableWidget, 5,
                                  ["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])
        self.insert_data_in_table(self.dbservice.get_groups_for_display(), self.tablegroup, 3,
                                  ["ИД", "Группа", "Отдел"])
        self.insert_data_in_table(self.dbservice.get_departments_for_display(), self.tabledep, 2, ["ИД", "Отдел"])
        self.insert_data_in_table(self.dbservice.get_positions_for_display(), self.tablepos, 2, ["ИД", "Должность"])

    def insert_data_in_table(self, res, table, number_of_columns, columns_names):
        table.setColumnCount(number_of_columns)
        table.setRowCount(0)
        table.setHorizontalHeaderLabels(columns_names)
        for i, row in enumerate(res):
            table.setRowCount(
                table.rowCount() + 1)
            for j, elem in enumerate(row):
                if elem is None:
                    elem = "Не назначено"
                table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.dbservice.close()

    def add(self):
        source = self.sender()
        if source == self.addemployee:
            self.child = EmployeeWindow(self.dbservice, WindowMode.insert, self)
            self.child.show()
        elif source == self.addgroup:
            self.child1 = GroupWindow(self.dbservice, WindowMode.insert)
            self.child1.show()
        elif source == self.adddep:
            self.child2 = DepartmentWindow(self.dbservice, WindowMode.insert)
            self.child2.show()
        elif source == self.addpos:
            self.child3 = PositionWindow(self.dbservice, WindowMode.insert)
            self.child3.show()

    def edit_employees(self):
        ID = self.get_id_by_row(self.tableWidget)
        if ID:
            employee = self.dbservice.get_employee(ID)
            try:
                cur_group_title = self.dbservice.get_group(employee.groupid).title
            except:
                cur_group_title = None
            try:
                cur_pos_title = self.dbservice.get_position(employee.positionid).title
            except:
                cur_pos_title = None
            self.child = EmployeeWindow(self.dbservice, WindowMode.update, ID, employee, cur_group_title, cur_pos_title)
            self.child.show()

    def edit_groups(self):
        ID = self.get_id_by_row(self.tablegroup)
        if ID:
            group = self.dbservice.get_group(ID)
            try:
                res = self.dbservice.get_department(group.departmentid).title
            except:
                res = None
            self.child1 = GroupWindow(self.dbservice, WindowMode.update, ID, group.title, res)
            self.child1.show()

    def edit_departments(self):
        ID = self.get_id_by_row(self.tabledep)
        if ID:
            department = self.dbservice.get_department(ID)
            self.child2 = DepartmentWindow(self.dbservice, WindowMode.update, ID, department.title)
            self.child2.show()

    def edit_positions(self):
        ID = self.get_id_by_row(self.tablepos)
        if ID:
            position = self.dbservice.get_position(ID)
            self.child3 = PositionWindow(self.dbservice, WindowMode.update, ID, position.title)
            self.child3.show()

    def delete_employee(self):
        ID = self.get_id_by_row(self.tableWidget)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элементы с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_item(Employee(ID, "", None, -1, -1, ""))
                self.select_data()

    def delete_group(self):
        ID = self.get_id_by_row(self.tablegroup)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элемент с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_item(Group(ID, "", -1))
                self.select_data()

    def delete_department(self):
        ID = self.get_id_by_row(self.tabledep)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элемент с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_item(Department(ID, ""))
                self.select_data()

    def delete_position(self):
        ID = self.get_id_by_row(self.tablepos)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элемент с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_item(Position(ID, ""))
                self.select_data()

    def sorting_emp(self):
        text1 = self.sort1_emp.currentText()
        text2 = self.sort2_emp.currentText()
        res = self.dbservice.sort_item(self.dbservice.employees, text1, text2)
        self.insert_data_in_table(res, self.tableWidget,
                                  5, ["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])

    def sorting_gr(self):
        text1 = self.sort1_gr.currentText()
        text2 = self.sort2_gr.currentText()
        res = self.dbservice.sort_item(self.dbservice.groups, text1, text2)
        self.insert_data_in_table(res, self.tablegroup,
                                  3, ["ИД", "Группа", "Отдел"])

    def sorting_dep(self):
        text1 = self.sort1_dep.currentText()
        text2 = self.sort2_dep.currentText()
        res = self.dbservice.sort_item(self.dbservice.departments, text1, text2)
        self.insert_data_in_table(res, self.tabledep,
                                  2, ["ИД", "Отдел"])

    def sorting_pos(self):
        text1 = self.sort1_pos.currentText()
        text2 = self.sort2_pos.currentText()
        res = self.dbservice.sort_item(self.dbservice.positions, text1, text2)
        self.insert_data_in_table(res, self.tablepos, 2, ["ИД", "Должность"])

    def find_employee(self):
        search_text = self.search_line.text()
        result = self.table_employees.findItems(search_text, QtCore.Qt.MatchStartsWith)
        rows = []
        if search_text:
            for item in result:
                id_row_search_text = self.gibr(item.row(), self.table_employees)
                row = self.dbservice.get_employee(id_row_search_text)
                dob = row.dob.strftime("%d.%m.%Y")
                group = self.dbservice.get_group(row.groupid).title
                position = self.dbservice.get_position(row.positionid).title
                full_row = (row.id, row.fullname, dob, group, position, row.picture)
                if full_row not in rows:
                    rows.append(full_row)
            self.tableWidget.clear()
            self.insert_data_in_table(rows, self.tableWidget, 5, ["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])
        else:
            self.select_data()

    def gibr(self, row, table):
        ID = False
        if row >= 0:
            fl = table.item(row, 0).text()
            ID = int(fl)
        return ID


class EmployeeWindow(QDialog):

    def __init__(self, dbservice: EmployeesDBService, mode: WindowMode, ID=None, employee=None, cur_group_title=None,
                 cur_pos_title=None, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog.ui', self)
        self.dbservice = dbservice
        self.groups = self.dbservice.get_groups()
        self.positions = self.dbservice.get_positions()
        self.update_combo()
        self.lineEdit.textChanged.connect(self.on_text_changed)
        if employee:
            self.lineEdit.setText(employee.fullname)
            self.dateEdit.setDate(employee.dob)
            self.picture = employee.picture
        else:
            self.picture = None
        if ID:
            self.ID = ID
        if cur_group_title:
            self.comboBox.setCurrentText(cur_group_title)
        if cur_pos_title:
            self.comboBox_2.setCurrentText(cur_pos_title)
        self.mode = mode
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def update_combo(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        result = [g.title for g in self.groups]
        for i in result:
            self.comboBox.addItem(i)
        result = [p.title for p in self.positions]
        for i in result:
            self.comboBox_2.addItem(i)

    def dialog(self):
        fullname = self.lineEdit.text()
        if fullname != "":
            DOB = self.dateEdit.text()
            cur_group_title = self.comboBox.currentText()
            cur_position_title = self.comboBox_2.currentText()

            groupid = -1
            for i in self.groups:
                if i.title == cur_group_title:
                    groupid = i.id

            positionid = -1
            for i in self.positions:
                if i.title == cur_position_title:
                    positionid = i.id

            if self.mode == WindowMode.insert:
                self.dbservice.add_item(Employee(-1, fullname, DOB, groupid, positionid, self.picture))
            else:
                self.dbservice.update_item(Employee(self.ID, fullname, DOB, groupid, positionid, self.picture))
            window.select_data()

    def mybutton_clicked(self):
        options = QFileDialog.Options()
        self.picture, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                      options=options)


class GroupWindow(QDialog):
    def __init__(self, dbservice: EmployeesDBService, mode: WindowMode, ID=None, title=None, cur_text=None,
                 parent=None):
        super().__init__(parent)
        uic.loadUi('dialog1.ui', self)
        self.dbservice = dbservice
        self.departments = self.dbservice.get_departments()
        self.update_combo()
        self.lineEdit.textChanged.connect(self.on_text_changed)
        if title:
            self.lineEdit.setText(title)
        if cur_text:
            self.comboBox.setCurrentText(cur_text)
        self.mode = mode
        self.ID = ID
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def update_combo(self):
        self.comboBox.clear()
        result = [d.title for d in self.departments]
        for i in result:
            self.comboBox.addItem(i)

    def dialog(self):
        title = self.lineEdit.text()
        if title != "":

            cur_dep_title = self.comboBox.currentText()
            departmentid = -1

            for i in self.departments:
                if i.title == cur_dep_title:
                    departmentid = i.id

            if self.mode == WindowMode.insert:
                self.dbservice.add_item(Group(-1, title, departmentid))
            else:
                self.dbservice.update_item(Group(self.ID, title, departmentid))
            window.select_data()


class BaseWindow(QDialog):
    def __init__(self, dbservice: EmployeesDBService, mode: WindowMode, id=None, title=None, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog2.ui', self)
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.mode = mode
        self.ID = id
        if title:
            self.lineEdit.setText(title)
        self.dbservice = dbservice
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))


class DepartmentWindow(BaseWindow):

    def dialog(self):
        self.title = self.lineEdit.text()
        if self.title != "":
            if self.mode == WindowMode.insert:
                self.dbservice.add_item(Department(-1, self.title))
            else:
                self.dbservice.update_item(Department(self.ID, self.title))
        window.select_data()


class PositionWindow(BaseWindow):

    def dialog(self):
        self.title = self.lineEdit.text()
        if self.title != "":
            if self.mode == WindowMode.insert:
                self.dbservice.add_item(Position(-1, self.title))
            else:
                self.dbservice.update_item(Position(self.ID, self.title))
        window.select_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
