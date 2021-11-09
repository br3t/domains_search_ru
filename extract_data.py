import gzip
import io
import csv

from requests_html import HTMLSession


class GetDomains:
    def __init__(self, res_file):
        """
        :param res_file: result CSV filename
        :type res_file: str
        """
        self.res_file = res_file

    @staticmethod
    def get_archive(url):
        """
        Extract GZ archive data by URL
        :param url: GZ archive URL
        :type url: str
        :return: All domains
        :rtype: bytes
        """
        try:
            session = HTMLSession()
            r = session.get(url)
            all_domains = gzip.open(io.BytesIO(r.content))
            return all_domains
        except Exception as e:
            print('get_archive func error: ', e, type(e))

    def domains_to_csv(self, data):
        """
        Decode bytes data and write to CSV
        :param data:
        :type data:
        """
        with open(self.res_file, 'a', encoding='utf-8', newline='') as res:
            my_csv = csv.writer(res, delimiter='\t')
            for row in data:
                my_csv.writerow(row.decode().strip().split('\t'))

    def worker(self, data_links):
        """
        Extract and write data to CSV
        :param data_links: A dict with zones as keys and links to GZ archives as values
        :type data_links: dict
        """
        with open(self.res_file, 'w', encoding='utf-8', newline='') as res:
            my_csv = csv.writer(res, delimiter='\t')
            header = ["domain", "registered", "date_created", "paid_till", "date_free", "delegated"]
            my_csv.writerow(header)
        for key in data_links:
            print(f'Download started ({key} zone). Please wait')
            archive = self.get_archive(data_links[key])
            self.domains_to_csv(archive)


if __name__ == "__main__":
    all_archives = {'ru': 'https://partner.r01.ru/zones/ru_domains.gz',
                    'rf': 'https://partner.r01.ru/zones/rf_domains.gz',
                    'su': 'https://partner.r01.ru/zones/su_domains.gz'}

    get_domains = GetDomains('all_domains.csv')
    get_domains.worker(all_archives)
