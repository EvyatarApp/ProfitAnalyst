import pandas as pd
from datetime import datetime


class ExcelCreator:

    def __init__(self, path_to_export):
        self.path_to_export = path_to_export

    def create_monthly_excel(self, number_of_years: int):

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

        df.to_excel(self.path_to_export)

    def create_daily_excel(self):

        current_date = datetime.now()
        formatted_date = [current_date.strftime("%d-%m-%Y")]

        df = pd.DataFrame({"DATE": formatted_date, "TOTAL_PROFIT": None})

        df.to_excel(self.path_to_export)