import re
import pandas as pd


class FindDomains:
    def __init__(self, base_file, res_file):
        """
        :param base_file: All domains data got CSV filename
        :type base_file: str
        :param res_file: Result CSV filename
        :type res_file: str
        """
        self.dataframe = pd.read_csv(base_file, delimiter='\t')
        self.res_file = res_file
        pd.options.mode.chained_assignment = None
        pd.set_option('display.max_rows', None)

    @staticmethod
    def filter_days_left(df, days):
        """
        Filter by domain free date
        :param df: DataFrame
        :type df:
        :param days: Days left to free date
        :type days: int
        :return: Filtered by date free DataFrame
        """
        df['date_free'] = pd.to_datetime(df['date_free'], format="%d.%m.%Y")
        df['days_left'] = (df['date_free'] - pd.to_datetime('today')).dt.days
        df_filtered = df.loc[df['days_left'] < days]
        df_filtered['date_created'] = pd.to_datetime(df_filtered['date_created'], format="%d.%m.%Y")
        df_filtered['domain_age'] = (pd.to_datetime('today') - df_filtered['date_created']).dt.days
        return df_filtered

    @staticmethod
    def search_by_name(df, query):
        """
        Find domains by mask or regex
        :param df: DataFrame
        :type df:
        :param query: Search term or RegEx
        :type query: str
        :return: DataFrame
        """
        filtered_df = df.loc[df['domain'].str.contains(query, flags=re.I, regex=True)]
        return filtered_df

    def worker(self, days, query):
        filtered_by_date = self.filter_days_left(self.dataframe, days)
        filtered_by_query = self.search_by_name(filtered_by_date, query)
        filtered_by_query.to_csv(self.res_file, sep='\t', index=False)
        print(f"Check {self.res_file}\n"
              f"Found domains:\n "
              f"{filtered_by_query['domain'].to_string(index=False)}")


if __name__ == '__main__':
    days_free = int(input('Enter days left number: ').strip())
    search_mask = input('Enter domains search mask (word or RegEx): ').strip()
    base_file = 'all_domains.csv'
    res_file = 'result.csv'
    domains_tools = FindDomains(base_file, res_file)
    domains_tools.worker(days_free, search_mask)
