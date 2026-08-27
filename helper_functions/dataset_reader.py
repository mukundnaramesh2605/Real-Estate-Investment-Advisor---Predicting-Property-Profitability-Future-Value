import pandas as pd

class dataset_reader:
    def __init__(self):
        self.df = pd.read_csv(r'Datasets/india_housing_prices_with_target_columns.csv')

    def get_data(self):
        return self.df 