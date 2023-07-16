from PyQt5.QtWidgets import (
    QApplication,
    QMenu,
    QTableWidget,
    QWidget,
    QHBoxLayout,
    QTableWidgetItem,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QMimeData
import xlsxwriter
import os
from PyQt5.QtGui import QDrag


class MyTableView(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setRowCount(10)
        # self.setColumnCount(3)

        # header_labels = ["Columna 1", "Columna 2", "Columna 3"]
        # self.setHorizontalHeaderLabels(header_labels)

        # for row in range(10):
        #     for col in range(3):
        #         item = QTableWidgetItem("Datos")
        #         self.setItem(row, col, item)

        self.selected_item = None

        self.setEditTriggers(QTableWidget.NoEditTriggers)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item is not None:
            self.selected_item = item
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_item is not None:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.selected_item.text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction)
        super().mouseMoveEvent(event)

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasText():
            item = self.itemAt(event.pos())
            if item is not None:
                item.setText(mime_data.text())
        super().dropEvent(event)
        
    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        export_action = context_menu.addAction("Exportar a Excel")
        copy_action = context_menu.addAction("Copiar")

        export_action.triggered.connect(self.export_to_excel)
        copy_action.triggered.connect(self.copy_cell)

        context_menu.exec_(self.mapToGlobal(pos))

    def export_to_excel(self):

        self.header_labels = [
            self.horizontalHeaderItem(i).text()
            for i in range(self.columnCount())
        ]
        workbook = xlsxwriter.Workbook("tabla.xlsx")
        worksheet = workbook.add_worksheet()


        for col in range(self.columnCount()):
            cell_value = self.header_labels[col]
            worksheet.write(0, col, cell_value)

        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item is not None:
                    worksheet.write(row + 1, col, item.text())

        workbook.close()
        os.startfile("tabla.xlsx")

    def copy_cell(self):
        selected = self.selectedRanges()[0]
        top = selected.topRow()
        bottom = selected.bottomRow()
        left = selected.leftColumn()
        right = selected.rightColumn()

        text = ""
        for row in range(top, bottom + 1):
            row_text = ""
            for col in range(left, right + 1):
                item = self.item(row, col)
                if item is not None and item.text() != "":
                    cell_text = item.text().replace("\n", " ").replace("\t", " ")
                    row_text += cell_text + "\t"
                else:
                    row_text += "\t"
            text += row_text.rstrip() + "\n"

        clipboard = QApplication.clipboard()
        clipboard.setText(text)
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.table_widget = MyTableView()
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MyWidget()
    window.show()
    app.exec_()
