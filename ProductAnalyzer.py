import pandas as pd
import numpy as np
import re
from Global_Classes.MytableView import MyTableView
import numpy.ma as ma
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem,QPlainTextEdit

class DataAnalyzer:
    def __init__(self):
        self.weights = {
            'Price': 0.3,
            'LQS': 0.25,
            'Est. Monthly Sales': 0.2,
            'Est. Monthly Revenue': 0.15,
            'Reviews': 0.1
        }
        self.mean_values = None
        self.std_values = None

    def currency_to_float(self, currency_str):
        if not isinstance(currency_str, str):
            return currency_str

        number_str = re.sub(r'[^\d.]', '', currency_str)
        try:
            return float(number_str)
        except ValueError:
            return float('nan')

    def analyze_data(self, df):
        df.replace('N.A.', float('nan'), inplace=True)
        df['Est. Monthly Revenue'] = df['Est. Monthly Revenue'].apply(lambda x: self.currency_to_float(x))

        numeric_columns = ['Est. Monthly Revenue', 'Est. Monthly Sales', 'Fees', 'Net', 'Rank', 'Reviews', 'LQS', 'Sellers', 'Rating', 'Weight']
        date_columns = ['Date First Available']

        df['Price'] = df['Price'].str.replace('$', '')
        numeric_columns.append('Price')

        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        self.mean_values = df[self.weights.keys()].mean()
        self.std_values = df[self.weights.keys()].std()

        df['Success_Index'] = df.apply(self.calculate_success_index, axis=1)
        max_success_index = df['Success_Index'].max()
        df['Success_Index'] = df['Success_Index'] / max_success_index

        df['POS'] = df.apply(self.calculate_pos, axis=1)
        df['CI'] = [self.calculate_ci(df, index) for index in df.index]
        df['PI'] = df.apply(lambda row: self.calculate_pi(row['POS'], row['CI']), axis=1)

        total_market_monthly_revenue = df['Est. Monthly Revenue'].sum(skipna=True)
        df_clean = df.dropna(subset=['Est. Monthly Sales', 'Est. Monthly Revenue', 'Price'])

        if total_market_monthly_revenue != 0:
            proportional_mean_sales = (df_clean['Est. Monthly Sales'] * df_clean['Est. Monthly Revenue']).sum(skipna=True) / total_market_monthly_revenue
            proportional_mean_price = (df_clean['Price'] * df_clean['Est. Monthly Revenue']).sum(skipna=True) / total_market_monthly_revenue
        else:
            proportional_mean_sales = 0
            proportional_mean_price = 0

        num_buy_box_owners = df['Buy Box Owner'].nunique()
        num_registros = len(df)

        competitors_zero_sales = len(df[df['Est. Monthly Sales'] == 0])
        competitors_sales_gt_zero = len(df[df['Est. Monthly Sales'] > 0])
        current_year = pd.to_datetime('today').year
        df['Date First Available'] = pd.to_datetime(df['Date First Available'])
        new_competitors = len(df[df['Date First Available'].dt.year == current_year])
        avg_market_sales = df['Est. Monthly Sales'].mean()
        avg_revenue = df['Est. Monthly Revenue'].mean()
        mean_price = df['Price'].mean()
        most_used_price = df['Price'].mode()
        most_used_price = most_used_price.iloc[0] if not most_used_price.empty else None
        avg_lqs = df['LQS'].mean()
        num_brands = df['Brand'].nunique()
        avg_reviews = df['Reviews'].mean()
        top_10_selling = df.nlargest(10, 'Est. Monthly Sales')
        avg_reviews_top_10_selling = top_10_selling['Reviews'].mean()
        avg_sales_top_10_selling = top_10_selling['Est. Monthly Sales'].mean()
        bottom_10_selling = df.nsmallest(10, 'Est. Monthly Sales')
        avg_reviews_bottom_10_selling = bottom_10_selling['Reviews'].mean()
        avg_sales_bottom_10_selling = bottom_10_selling['Est. Monthly Sales'].mean()
        avg_rank = df['Rank'].mean()
        avg_fees = df['Fees'].mean()
        words = df['Product Name'].str.split(expand=True).stack()
        most_repeated_word = words.value_counts().idxmax()

        return df, num_buy_box_owners, proportional_mean_sales, proportional_mean_price, num_registros, competitors_zero_sales, competitors_sales_gt_zero, new_competitors, avg_market_sales, avg_revenue, mean_price, most_used_price, avg_lqs, num_brands, avg_reviews, avg_reviews_top_10_selling, avg_sales_top_10_selling, avg_reviews_bottom_10_selling, avg_sales_bottom_10_selling, avg_rank, avg_fees, most_repeated_word

    def calculate_success_index(self, row):
        success_index = 0
        for key, weight in self.weights.items():
            relative_diff = abs(row[key] - self.mean_values[key]) / self.std_values[key]
            success_index += relative_diff * weight
        return success_index

    def calculate_pos(self, row):
        lqs_score = row['LQS'] / 10
        reviews_score = 1 - (row['Reviews'] / (row['Reviews'] + 1))
        rating_score = row['Rating'] / 5
        sales_velocity = row['Est. Monthly Sales'] / max(1, (pd.Timestamp.now() - row['Date First Available']).days)
        sales_velocity_score = sales_velocity / (sales_velocity + 1)
        pos = lqs_score * reviews_score * rating_score * sales_velocity_score
        return pos

    def calculate_ci(self, df, index):
        row = df.loc[index]
        rank_score = 1 - (row['Rank'] / (row['Rank'] + 1))
        sellers_score = 1 - (row['Sellers'] / (row['Sellers'] + 1))
        price_var_score = 1 - abs(row['Price'] - df['Price'].mean()) / df['Price'].std()
        ci = rank_score * sellers_score * price_var_score
        return ci

    def calculate_pi(self, pos, ci, pos_weight=0.5, ci_weight=0.5):
        pi = pos_weight * pos + ci_weight * ci
        return pi
