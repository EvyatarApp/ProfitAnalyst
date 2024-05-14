import pandas as pd
import matplotlib.pyplot as plt



class Dashboard:

    def __init__(self, path, stocks_value_sheet, deposit_monitoring_sheet, date_column=None):
        self.path = path
        self.stocks_value_sheet = stocks_value_sheet
        self.deposit_monitoring_sheet = deposit_monitoring_sheet
        self.date_column = date_column
        if not self.date_column:
            self.date_column = input("Please insert your date column")
        self.stocks_dataframe = self._get_df(self.stocks_value_sheet)
        self.deposits_dataframe = self._get_df(self.deposit_monitoring_sheet)
        self.display_dataframe = pd.DataFrame(index=["MONTHLY_PROFIT", "TOTAL_PROFIT", "PERCENTAGE"])
        self.display_dataframe = self._get_data()

    def show_data(self):
        print(self.display_dataframe)

    def _get_data(self):
        self._get_monthly_profit_data()
        self._get_total_profit_data()
        self._get_percentage()
        return self.display_dataframe



    def show_profit_graphs(self):
        plt.style.use("ggplot")
        plt.figure(figsize=(10, 8))

        plt.subplot(1, 2, 1)
        first_plot = self.display_dataframe.T.MONTHLY_PROFIT.round(2).plot(kind="bar", title="MONTHLY PROFIT")
        for p in first_plot.patches:
            first_plot.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plt.subplot(1, 2, 2)
        second_plot = self.display_dataframe.T.TOTAL_PROFIT.round(2).plot(kind="bar", title="TOTAL PROFIT")
        for p in second_plot.patches:
            second_plot.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                 ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        plt.show()

    def show_stock_graphs(self):
        stocks_dataframe = self.stocks_dataframe.copy()
        deposits_dataframe = self.deposits_dataframe.copy()
        stocks_dataframe.drop(index=stocks_dataframe.index[0])
        stocks_dataframe.index = pd.to_datetime(stocks_dataframe.index)

        for column in deposits_dataframe.columns:
            deposits_dataframe[column] = deposits_dataframe[column].cumsum()

        for column in list(stocks_dataframe.columns):
            stocks_dataframe[column] = stocks_dataframe[column] - stocks_dataframe[column].iat[0]

        stocks_dataframe -= deposits_dataframe

        num_of_columns = len(stocks_dataframe.columns)
        num_of_plots = num_of_columns / 2
        if num_of_plots % 2 != 0:
            num_of_plots += 0.5

        plt.figure(figsize=(20, 20))

        index = 1
        for column in stocks_dataframe.columns:
            plt.subplot(int(num_of_plots), 2, index)
            index += 1
            stocks_dataframe[column].plot(title=column)
            plt.xticks(list(stocks_dataframe.index), [x.strftime('%Y-%m-%d') for x in stocks_dataframe.index], rotation=45)

        plt.tight_layout()

        plt.show()

    def _get_percentage(self):
        total_money = self.stocks_dataframe.iloc[-1].sum()
        percentage_dataframe = self.stocks_dataframe.iloc[-1]
        for column in list(percentage_dataframe.index):
            self.display_dataframe.loc["PERCENTAGE", column] = round(percentage_dataframe.loc[column] / total_money, 2)

    def _get_monthly_profit_data(self):
        monthly_profit_dataframe = pd.DataFrame(self.stocks_dataframe.diff().iloc[-1] - self.deposits_dataframe.iloc[-1])
        for column in list(monthly_profit_dataframe.index):
            self.display_dataframe.loc["MONTHLY_PROFIT", column] = monthly_profit_dataframe.loc[column][0]

    def _get_total_profit_data(self):
        total_profit_dataframe = pd.DataFrame(
            self.stocks_dataframe.iloc[-1] - self.stocks_dataframe.iloc[0] - self.deposits_dataframe.sum())
        for column in list(total_profit_dataframe.index):
            self.display_dataframe.loc["TOTAL_PROFIT", column] = total_profit_dataframe.loc[column][0]

    def _get_df(self, sheet_name):

        if not self.path.endswith("xlsx"):
            raise AttributeError("Input path is not valid (should end with xlsx)")

        df = pd.read_excel(self.path, sheet_name=sheet_name)

        df.set_index(self.date_column, inplace=True)

        return df


if __name__ == "__main__":
    launch = Dashboard(
        path="https://docs.google.com/spreadsheets/d/e/2PACX-1vTJGx5xFkdOex_STmQwjqIbwfZPmtfxwXt_VyW2ssArN1AZLsvSkVYbdCPtdEBshFpl_v4uksizOb-T/pub?output=xlsx",
        stocks_value_sheet="Monitoring",
        deposit_monitoring_sheet="Depositing",
        date_column="DATE"
    )

    launch.show_profit_graphs()