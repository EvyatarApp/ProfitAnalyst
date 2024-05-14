import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


class ProfitMonitor:

    def __init__(self, path: str, date_column=None, profit_column=None):
        self.path = path
        self.date_column = date_column
        self.profit_column = profit_column
        self.df = self.get_df()

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

    def generate_top_5_highest_profit_dates(self):
        self.generic_generate(
            df=self.df,
            sort_by="TOTAL_PROFIT",
            number_of_rows=5,
            string_search="profit",
            ascending=False
        )

    def generate_top_5_lowest_profit_dates(self):
        self.generic_generate(
            df=self.df,
            sort_by="TOTAL_PROFIT",
            number_of_rows=5,
            string_search="profit",
        )

    def generate_top_5_highest_returns_dates(self):
        self.generic_generate(
            df=self.df,
            sort_by="RETURN",
            number_of_rows=5,
            string_search="return",
            ascending=False)

    def generate_top_5_lowest_returns_dates(self):
        self.generic_generate(
            df=self.df,
            sort_by="RETURN",
            number_of_rows=5,
            string_search="return"
        )

    @staticmethod
    def generic_generate(df, sort_by, number_of_rows, string_search, ascending=True):
        for i, row in df.sort_values(sort_by, ascending=ascending).head(number_of_rows).iterrows():
            print(f"on {row['DATE']} your {string_search} was {row[sort_by]} shekels")

    def get_return_hist(self):
        plt.figure(figsize=(20,20))
        plt.style.use("fivethirtyeight")
        plt.hist(self.df.RETURN)
        plt.show()

    def get_df(self) -> DataFrame:

        if self.path.endswith("csv"):
            df = pd.read_csv(self.path)
        elif self.path.endswith("xlsx"):
            df = pd.read_excel(self.path)

        else:
            raise ValueError("Your excel or csv path is not valid")

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

        df.dropna(subset="TOTAL_PROFIT", inplace=True)
        df["RETURN"] = df["TOTAL_PROFIT"].diff()

        df["DATE"] = pd.to_datetime(df["DATE"], format="%d-%m-%Y", errors="coerce")
        df.dropna(subset="DATE", inplace=True)

        return df[["DATE", "TOTAL_PROFIT", "RETURN"]]

    def get_difference_between_dates(self, first_date, end_date):
        df = self.df
        df = df[df.DATE.between(first_date, end_date)]
        if len(df) == 0:
            raise ValueError(f"The excel / csv has no documentation between {first_date} and {end_date}")
        elif len(df) == 1:
            raise ValueError(f"The excel / csv has only one documentation between {first_date} and {end_date}.\nThere is nothing to calculate")
        else:
            difference = df.iloc[-1]["TOTAL_PROFIT"] - df.iloc[0]["TOTAL_PROFIT"]
            if difference >= 0:
                print(f"Between {first_date} and {end_date} you earned {difference} shekels")
            else:
                print(f"Between {first_date} and {end_date} you lost {difference} shekels")


if __name__ == "__main__":
    launch = ProfitMonitor(
        path=r"https://docs.google.com/spreadsheets/d/e/2PACX-1vQCwgfianjSsF8p8kSnVKYrMThJ7S7ouJu03SEKDbyKlYYWsVNSQ2mFZxy_4kSEF7tj6BoUJs8erGrH/pub?output=csv",
        date_column="date",
        profit_column="profit"
    )
    launch.get_return_hist()
