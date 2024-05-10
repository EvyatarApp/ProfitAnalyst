import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def _check_df(func):
    def wrapper(self, *args, **kwargs):
        if self.df is None:
            raise ValueError("No path to excel/csv was provided. Cannot execute this function.")
        return func(self, *args, **kwargs)

    return wrapper


class ProfitMonitor:

    def __init__(self, path=None, date_column=None, profit_column=None):
        self.path = path
        self.date_column = date_column
        self.profit_column = profit_column
        self.df = self.get_df()
        self.df = self.fix_df()

    @staticmethod
    def create_monthly_excel(path_to_export: str, number_of_years: int):

        # Get current month and year
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        # Generate dates for every month starting from the current month for 50 years
        dates = []
        for year in range(current_year, current_year + number_of_years):
            for month in range(current_month, 13):
                dates.append(f"{month:02d}-{year}")
            current_month = 1  # Reset month to 1 for the next year

        # Create DataFrame
        df = pd.DataFrame({"DATE": dates, "TOTAL_PROFIT": None})

        df.to_excel(path_to_export)

    @staticmethod
    def create_daily_excel(path_to_export: str):

        current_date = datetime.now()
        formatted_date = [current_date.strftime("%d-%m-%Y")]

        df = pd.DataFrame({"DATE": formatted_date, "TOTAL_PROFIT": None})

        df.to_excel(path_to_export)

    @_check_df
    def generate_all_time_line_graph(self):
        df = self.df
        df.set_index("DATE", inplace=True)
        plt.figure(figsize=(20, 20))
        plt.style.use('fivethirtyeight')
        plt.xlabel("Date")
        plt.ylabel("Profit")
        df.index = pd.to_datetime(df.index, format="%d-%m-%Y")
        plt.plot(df.TOTAL_PROFIT)

        plt.show()

    @_check_df
    def generate_top_5_highest_profit_dates(self):
        self.generic_generate(
            sort_by="TOTAL_PROFIT",
            number_of_rows=5,
            string_search="profit",
            ascending=False
        )

    @_check_df
    def generate_top_5_lowest_profit_dates(self):
        self.generic_generate(
            sort_by="TOTAL_PROFIT",
            number_of_rows=5,
            string_search="profit",
        )

    @_check_df
    def generate_top_5_highest_returns_dates(self):
        self.generic_generate(
            sort_by="PROFIT_CHANGE",
            number_of_rows=5,
            string_search="return",
            ascending=False)

    @_check_df
    def generate_top_5_lowest_returns_dates(self):
        self.generic_generate(
            sort_by="PROFIT_CHANGE",
            number_of_rows=5,
            string_search="return"
        )

    def generic_generate(self, sort_by, number_of_rows, string_search, ascending=True):
        df = self.df
        for i, row in df.sort_values(sort_by, ascending=ascending).head(number_of_rows).iterrows():
            print(f"on {row['DATE']} your {string_search} was {row[sort_by]}")

    def get_df(self) -> pd.DataFrame:

        if self.path is None:
            return None

        elif self.path.endswith("csv"):
            df = pd.read_csv(self.path)
        elif self.path.endswith("xlsx"):
            df = pd.read_excel(self.path)

        else:
            raise ValueError("Your excel or csv path is not valid")

        return df

    def fix_df(self) -> pd.DataFrame:

        df = self.df

        if df is None:
            return None

        if "DATE" not in df.columns:
            date_column = self.date_column
            if self.date_column is None:
                date_column = input("Please insert the name of your excel's date column")

            df.rename(columns={date_column: "DATE"}, inplace=True)

        if "TOTAL_PROFIT" not in df.columns:
            profit_column = self.profit_column
            if self.profit_column is None:
                profit_column = input("Please insert the name of your excel's total profit column")

            df.rename(columns={profit_column: "TOTAL_PROFIT"}, inplace=True)

        df.dropna(subset="TOTAL_PROFIT",inplace=True)
        df["PROFIT_CHANGE"] = df["TOTAL_PROFIT"].diff()

        print("Your dataframe is valid for all functions")
        return df[["DATE", "TOTAL_PROFIT", "PROFIT_CHANGE"]]


if __name__ == "__main__":
    launch = ProfitMonitor(
        path=r"https://docs.google.com/spreadsheets/d/e/2PACX-1vQCwgfianjSsF8p8kSnVKYrMThJ7S7ouJu03SEKDbyKlYYWsVNSQ2mFZxy_4kSEF7tj6BoUJs8erGrH/pub?output=csv",
        date_column="date",
        profit_column="profit"
    )
    launch.generate_top_5_lowest_profit_dates()
    launch.generate_top_5_highest_profit_dates()
    launch.generate_top_5_highest_returns_dates()
    launch.generate_top_5_lowest_returns_dates()
