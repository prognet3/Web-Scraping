import requests
from bs4 import BeautifulSoup
import time

try:

    class CheckSubchannel:
        url = "https://www.uceprotect.net/en/rblcheck.php"
        '#Check subchannel automatically'
        def subchannelid(self):
            website_content = requests.get(self.url)
            html_content = BeautifulSoup(website_content.text, 'html.parser')
            subchannel_id = html_content.find('input', {'name': 'subchannel'}).get('value')
            return subchannel_id


    class UceProtect(CheckSubchannel):
        def __init__(self, whattocheck, ipr):
            self.whattocheck = whattocheck
            self.ipr = ipr

        def serviceprovider_content(self):

            content_final = {
                'whattocheck': str(self.whattocheck),
                'ipr': int(self.ipr),
                'subchannel': self.subchannelid()
                            }
            result = requests.post(self.url, data=content_final)
            result_text = result.text
            extract_attribute_classdb = BeautifulSoup(result_text, 'html.parser')
            main_table = extract_attribute_classdb('table', attrs={'class': "db"})
            main_tr = main_table[0].find_all('tr')
            primary_list = []
            file_foremail = open("emailfile.txt", 'w+')
            for td_list in range(len(main_tr)):
                main_td = main_tr[td_list].find_all('td')
                first_second_td = main_td[0:2]
                for check_strongtag in range(len(first_second_td)):
                    strong_tag = first_second_td[check_strongtag].find_all('strong')
                    for textfile in strong_tag:
                        text_file = str(textfile.text)
                        replace_twospace = text_file.replace('  ', '')
                        without_subnetword = replace_twospace.replace('Subnet - ', '')
                        primary_list.append(without_subnetword)
            final_list = []
            for exclude_notavailable in range(len(primary_list)):
                if primary_list[exclude_notavailable] == "Not available at this time.":
                    continue
                else:
                    final_list.append(primary_list[exclude_notavailable])
            for ip_check in range(0, len(final_list), 2):
                create_tuple = final_list[ip_check], final_list[ip_check+1]
                if create_tuple[1] == 'NOT LISTED':
                    continue
                else:
                    print(create_tuple)
                    file_foremail.write(str(create_tuple))
                    file_foremail.write('\n')


    as_number = int(input("please enter AS-Number : "))
    test = UceProtect("ASN", as_number)
    test.serviceprovider_content()
    time.sleep(100)

except:
    print("Check your internet connection")

