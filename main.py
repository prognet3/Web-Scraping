# 'import Library'
import requests
from bs4 import BeautifulSoup
import time

try:
    '#Checking subchannel automatically'
    class Check_Subchannel:
        url = "https://www.uceprotect.net/en/rblcheck.php"

        def subchannelid_method(self):
            website_content = requests.get(self.url)
            html_content = BeautifulSoup(website_content.text, 'html.parser')
            subchannel_id = html_content.find('input', {'name': 'subchannel'}).get('value')
            return subchannel_id


    class UceProtect(Check_Subchannel):
        def __init__(self, whattocheck, ipr):
            self.whattocheck = whattocheck
            self.ipr = ipr

        # 'Send ASNumber and subchannel'
        # 'Finding needed IPs'
        def serviceprovider_content(self):
            content_final = {
                'whattocheck': str(self.whattocheck),
                'ipr': int(self.ipr),
                'subchannel': self.subchannelid_method()
                            }
            result = requests.post(self.url, data=content_final)
            result_text = result.text
            extract_attribute_classdb = BeautifulSoup(result_text, 'html.parser')
            main_table = extract_attribute_classdb('table', attrs={'class': "db"})
            main_tr = main_table[0].find_all('tr')
            primary_list = []
            file_for_email = open("emailfile.txt", 'w+')
            for td_list in range(len(main_tr)):
                main_td = main_tr[td_list].find_all('td')
                first_second_td = main_td[0:2]
                for check_strong_tag in range(len(first_second_td)):
                    strong_tag = first_second_td[check_strong_tag].find_all('strong')
                    for textfile in strong_tag:
                        text_file = str(textfile.text)
                        replace_two_space = text_file.replace('  ', '')
                        without_subnet_word = replace_two_space.replace('Subnet - ', '')
                        primary_list.append(without_subnet_word)
            final_list = []
            for exclude_not_available in range(len(primary_list)):
                if primary_list[exclude_not_available] == "Not available at this time.":
                    continue
                else:
                    final_list.append(primary_list[exclude_not_available])
            for ip_check in range(0, len(final_list), 2):
                create_tuple = final_list[ip_check], final_list[ip_check+1]
                if create_tuple[1] == 'NOT LISTED':
                    continue
                else:
                    # print(create_tuple)
                    print(f'prefix is {create_tuple[0]}, Status is {create_tuple[1]}')
                    file_for_email.write(str(create_tuple))
                    file_for_email.write('\n')


    as_number = int(input("please enter AS-Number : "))
    test = UceProtect("ASN", as_number)
    test.serviceprovider_content()
    time.sleep(100)

except:
    print("Check your internet connection")

