import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QTableWidgetItem, QPushButton, QFileDialog, QLabel, QTextEdit, QTableWidget, QHeaderView,QHBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd
from Global_Classes.MytableView import MyTableView
import re
import numpy as np
from numpy import ma
from Calculations.ProductAnalyzer import DataAnalyzer


class ProductAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.data_analyzer = DataAnalyzer()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Amazon FBA Product Analyzer")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.import_button = QPushButton("Import Excel File", self)
        self.import_button.clicked.connect(self.import_excel)

        self.append_button = QPushButton("Add Data", self)
        self.append_button.clicked.connect(self.append_data)

        self.validate_button = QPushButton("Validate and Analyze Data", self)
        self.validate_button.clicked.connect(self.validate_and_analyze)

        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.append_button)
        button_layout.addWidget(self.validate_button)

        self.table = MyTableView()
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels(['Est. Monthly Revenue', 'Est. Monthly Sales', 'Price', 'Fees', 'Net', 'Rank', 'Reviews', 'LQS', 'Sellers', 'Rating', 'Weight', 'POS', 'CI', 'PI'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.result_label = QLabel("Analysis Results:")
        self.result_label.setAlignment(Qt.AlignLeft)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def import_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel file", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.load_data(file_name)

    def load_data(self, file_name):
        df = pd.read_excel(file_name)
        self.df_to_table(df)

    def df_to_table(self, df, append=False):
        if not append:
            self.table.setRowCount(len(df))
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(df.columns)
        else:
            current_rows = self.table.rowCount()
            self.table.setRowCount(current_rows + len(df))

        for i in range(len(df)):
            for j in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iat[i, j]))
                if not append:
                    self.table.setItem(i, j, item)
                else:
                    self.table.setItem(current_rows + i, j, item)

    def append_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel file", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            df_append = pd.read_excel(file_name)
            self.df_to_table(df_append, append=True)

    def validate_and_analyze(self):
        df = self.table_to_df()
        analyzed_df, num_buy_box_owners, proportional_mean_sales, proportional_mean_price, num_registros, competitors_zero_sales, competitors_sales_gt_zero, new_competitors, avg_market_sales, avg_revenue, mean_price, most_used_price, avg_lqs, num_brands, avg_reviews, avg_reviews_top_10_selling, avg_sales_top_10_selling, avg_reviews_bottom_10_selling, avg_sales_bottom_10_selling, avg_rank, avg_fees, most_repeated_word = self.data_analyzer.analyze_data(df)
        self.df_to_table(analyzed_df)
        self.display_analysis_results(num_buy_box_owners, proportional_mean_sales, proportional_mean_price, num_registros, competitors_zero_sales, competitors_sales_gt_zero, new_competitors, avg_market_sales, avg_revenue, mean_price, most_used_price, avg_lqs, num_brands, avg_reviews, avg_reviews_top_10_selling, avg_sales_top_10_selling, avg_reviews_bottom_10_selling, avg_sales_bottom_10_selling, avg_rank, avg_fees, most_repeated_word)

    def table_to_df(self):
        df = pd.DataFrame(columns=[self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())])
        for row in range(self.table.rowCount()):
            row_items = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item is not None:
                    row_items.append(item.text())
                else:
                    row_items.append('')
            df = df.append(pd.Series(row_items, index=df.columns), ignore_index=True)
        return df

    def display_analysis_results(self, num_buy_box_owners, proportional_mean_sales, proportional_mean_price, num_registros, competitors_zero_sales, competitors_sales_gt_zero, new_competitors, avg_market_sales, avg_revenue, mean_price, most_used_price, avg_lqs, num_brands, avg_reviews, avg_reviews_top_10_selling, avg_sales_top_10_selling, avg_reviews_bottom_10_selling, avg_sales_bottom_10_selling, avg_rank, avg_fees, most_repeated_word):
        analysis_result = f"""
            Número de registros: {num_registros}
            Número de competidores: {num_buy_box_owners}
            Competidores con venta 0: {competitors_zero_sales}
            Competidores con venta mayores de 0: {competitors_sales_gt_zero}
            Competidores nuevos (año actual): {new_competitors}
            Venta media del mercado: {avg_market_sales}
            Precio más usado: {most_used_price}
            Precio medio: {mean_price}
            LQS medio: {avg_lqs}
            Numero de marcas: {num_brands}
            Media de comentarios: {avg_reviews}
            Media de comentarios de los 10 competidores que más venden: {avg_reviews_top_10_selling}
            Venta media de competidores que más venden: {avg_sales_top_10_selling}
            Media de comentarios de los 10 competidores que menos venden: {avg_reviews_bottom_10_selling}
            Venta media de competidores que menos venden: {avg_sales_bottom_10_selling}
            Rango medio: {avg_rank}
            Gastos medios: {avg_fees}
            Palabra más repetida: {most_repeated_word}
            Venta media del mercado proporcional: {proportional_mean_sales}
            Precio medio ponderado: {proportional_mean_price}
            """

        self.result_text.setPlainText(analysis_result)