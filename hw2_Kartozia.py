#буква И
import re
from lxml import etree
from lxml import html
import requests


prof_page = requests.get('https://www.hse.ru/org/persons/?ltr=И;udept=22726')  

#etree




        
       
class Professor:
    def __init__ (self, page):
        self.etree = self.teachers_with_etree(page)
        self.xpath = self.teachers_with_xpath(page)
        
    def get_email(self, raw_mail):
        raw_mail = str(raw_mail)
        raw_mail = raw_mail.replace ('-at-', '@')
        raw_mail = raw_mail.replace('","', '')
        raw_mail = raw_mail.replace('["', '')
        final_email = raw_mail.replace('"]', '')
        return final_email

    def teachers_with_etree(self, page):
        prof_arr = []
        root = etree.HTML(page.content)
        persons = root[1][1][3][2][1][0][2][1]
        for p in persons:
            if 'post person' in p.attrib['class']:
                head = p[0]
                post_content = head[1][0]
                extra_small = head[0]
                if len(extra_small) > 2:
                    main_phone = extra_small[0].text
                    email = extra_small[2].attrib
                    final_email = self.get_email(email)
                if len(post_content) > 2:
                    full_name = post_content[0][0].attrib
                    post = post_content[1][0].text
                    where = post_content[1][0][0].text
                    science = post_content[2][0].text
                else:
                    full_name = post_content[0][0].attrib
                    post = post_content[1][0].text
                if len(post_content[1][0]) > 1:
                    where = post_content[1][0][0].text
#                name = re.findall('<div class="g-pic person-avatar-small2" title="(.+?)" alt=', full_name)
                #fname = name.group(1)    
                prof_arr.append(str(full_name)+ '\n Phone:'+ str(main_phone) + '\n E-mail:' + final_email + '\n' + str(post) + ' ' + str(where))
                return prof_arr[:1]

    def teachers_with_xpath(self, page):
        prof_arr = []
        workplace = {}
        tree = html.fromstring(page.content)
        persons = tree.xpath('//div[@class="post person"]')
        for p in persons:
            name = p.xpath('.//a[@href and @class="link link_dark large b"]/div[@class="g-pic person-avatar-small2"]/@title')
            phone = p.xpath('.//div[@class="l-extra small"]/span/text()')
            email = p.xpath('.//div[@class="l-extra small"]/a[@class="link"]/@data-at')
            final_email = self.get_email(email)
            post = p.xpath('.//p[@class="with-indent7"]/span/text()')  # нужно убрать табуляцию и концы строчек
            where = p.xpath('.//p[@class="with-indent7"]/span/a/text()')
            science = p.xpath('.//div[@class="with-indent small"]/a/text()')
            prof_arr.append(str(name)+ '\n Phone:'+ str(phone) + '\n E-mail:' + final_email + '\n' + str(post) + ' ' + str(where) + '\nИнтересы: ' + str(science))
        return prof_arr

    
hse_prof = Professor(prof_page)
result = hse_prof.etree
for i in result:
    print(i)
prof_page.close()
