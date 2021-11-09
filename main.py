import os

from extract_data import GetDomains
from domains_tools import FindDomains


def check_data_file(file):
    """
    Check CSV file with data and initiate parse data if file not found or needs to update.
    """
    all_archives = {'ru': 'https://partner.r01.ru/zones/ru_domains.gz',
                    'rf': 'https://partner.r01.ru/zones/rf_domains.gz',
                    'su': 'https://partner.r01.ru/zones/su_domains.gz'}
    if file not in os.listdir():
        get_domains = GetDomains(file)
        get_domains.worker(all_archives)
    else:
        while True:
            choice = input('Do you want UPDATE CSV file? (YES/NO)\n').strip().lower()
            if choice == 'yes':
                get_domains = GetDomains(file)
                get_domains.worker(all_archives)
            elif choice == 'no':
                break
            else:
                print('Please enter YES or NO')
    return file


base_file = 'all_domains.csv'
res_file = 'result.csv'

work_file = check_data_file(base_file)

days_free = int(input('Enter days left number: ').strip())
search_mask = input('Enter domains search mask (word or RegEx): ').strip()

domains_tools = FindDomains(work_file, res_file)
domains_tools.worker(days_free, search_mask)

