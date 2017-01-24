#буква И
import re
    
class Professor:
    def __init__(self, html):
        self.work = self.get_info(html)
        self.surname = self.get_surname(html)
        self.first_name = self.get_first_name(html)
        self.patronym = self.get_patronym(html)
        self.phone = self.get_phone(html)
        self.email = self.get_email(html)
        self.science = self.get_science(html)

    def get_info(self, html):
        work_place = {}
        work_info = re.search('<p class="with-indent7">(.+?)</p>', html, flags = re.DOTALL)
        work_info = work_info.group(1).replace('\t', '')
        span = re.findall('<span>(.+?)</span>', work_info, re.DOTALL)
        for i in span:
            post = re.search('\n(.+?)\n\n', i)
            where = re.findall('<a class="link" href=".+?">(.+?)</a>', i)
            work_place[post.group(1)] = where
        return work_place

    def get_surname (self, html):
        name = re.search('<div class="g-pic person-avatar-small2" title="(.+?)" alt=', html)
        full_name = name.group(1).split()
        surname = full_name[0]
        return surname
    
    def get_first_name (self, html):
        name = re.search('<div class="g-pic person-avatar-small2" title="(.+?)" alt=', html)
        full_name = name.group(1).split()
        first_name = full_name[1]
        return first_name
    
    def get_patronym (self, html):
        name = re.search('<div class="g-pic person-avatar-small2" title="(.+?)" alt=', html)
        full_name = name.group(1).split()
        if len(full_name) > 2:
            patronym = full_name[2]
            return patronym
        else:
            return ''

    def get_phone(self, html):
        phone = re.search('<div class="l-extra small">(.+?)<br/>', html, flags = re.DOTALL)
        if phone:
            phone_number = re.findall('<span>(.+?)</span>', phone.group(1), flags = re.DOTALL)
            return phone_number

    def get_email(self, html):
        email = re.search('<a class="link" data-at=(.+?)></a>', html)
        if email:
            raw_mail = email.group(1).replace ('-at-', '@')
            raw_mail = raw_mail.replace('","', '')
            raw_mail = raw_mail.replace('["', '')
            final_email = raw_mail.replace('"]', '')
            return final_email

    def get_science(self, html):
        sci = re.search('<div class="with-indent small">(.+?)</div>', html)
        if sci:
            interest = re.findall('<a class="tag" href=".+?">(.+?)</a>', sci.group(1))
            return interest
                                
        
html = open ('prof.html', 'r', encoding = "utf8-")
html_r = html.read()
prof_arr = []
persons = re.findall('<div class="post person">(.+?)\t\t\t</div>\n\t\t</div>\n\t</div>\n</div>', html_r, flags = re.DOTALL)

for p in persons:
    hse_prof = Professor(p)
    hse_prof.work
    hse_prof.surname
    hse_prof.first_name
    hse_prof.patronym
    hse_prof.phone
    hse_prof.email
    hse_prof.science
    prof_arr.append(hse_prof)
print(prof_arr)
    #print(hse_prof.fio, hse_prof.work,hse_prof.phone, hse_prof.email, hse_prof.science)
html.close()
