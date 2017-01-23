#буква И
import re
from lxml import etree
from lxml import html
import requests


prof_page = requests.get('https://www.hse.ru/org/persons/?ltr=И;udept=22726')  

#etree
root = etree.HTML(prof_page.content)
persons = root[1][1][3][2][1][0][2][1]
print(persons.attrib)

        
        
class Professor:
    def __init__ (self, page):
        self.etree = self.teachers_with_etree(page)
        self.xpath = self.teachers_with_xpath(page)

    def teachers_with_etree(self, page):
        prof_arr = []

    def get_email(self, raw_mail):
        raw_mail = str(raw_mail)
        raw_mail = raw_mail.replace ('-at-', '@')
        raw_mail = raw_mail.replace('","', '')
        raw_mail = raw_mail.replace('["', '')
        final_email = raw_mail.replace('"]', '')
        return final_email

    def teachers_with_xpath(self, page):
        prof_arr = []
        workplace = {}
        tree = html.fromstring(page.content)
        persons = tree.xpath('//div[@class="post person"]')
        for p in persons:
            name = p.xpath('.//a[@href and @class="link link_dark large b"]/div[@class="g-pic person-avatar-small2"]/@title')
            phone = p.xpath('.//div[@class="l-extra small"]/span/text()')
            email = p.xpath('.//div[@class="l-extra small"]/a[@class="link"]/@data-at') # пустой массив
            final_email = self.get_email(email)
            post = p.xpath('.//p[@class="with-indent7"]/span/text()')  # нужно убрать табуляцию и концы строчек
 #           clear = self.space_remove(post)
            where = p.xpath('.//p[@class="with-indent7"]/span/a/text()')
 #           workplace = self.work_place(posts)
            science = p.xpath('.//div[@class="with-indent small"]/a/text()')
            prof_arr.append(str(name)+ '\n Phone:'+ str(phone) + '\n E-mail:' + final_email + '\n' + str(post) + ' ' + str(where) + '\nИнтересы: ' + str(science))
        return prof_arr[:1]

    
##    def work_place (self, post):
##        workp ={}
##        for p in post:
##            where = p.xpath('/a/text()')
##            workp[p] = where
##        return workp

##    def space_remove (self, etw):
##        etw = str(etw)
##        etw = etw.replace('\t', '')
##        return etw
    
##hse_prof = Professor(prof_page)
##result = hse_prof.etree
##for i in result:
##    print(i)
prof_page.close()
