import requests
import re


class es_test:

    def __init__(self, school, username, password):
        if school.upper() == 'BNUZ':
            self.check = self.BNUZ_es_test(username, password)

    def result(self):
        return self.check

    def BNUZ_es_test(self, username, password):
        """北师珠教务登陆验证"""
        try:

            # 获取表单信息
            url = 'http://es.bnuz.edu.cn/default2.aspx'
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

            r = requests.get(url, headers=header)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text
            data = {
                "__EVENTTARGET": '',
                "__EVENTARGUMENT": '',
                "__VIEWSTATE": eval(re.findall('".*?"', re.findall('id="__VIEWSTATE" value=".*?" />', html)[0])[1]),
                "__VIEWSTATEGENERATOR": eval(
                    re.findall('".*?"', re.findall('id="__VIEWSTATEGENERATOR" value=".*?" />', html)[0])[1]),
                "__PREVIOUSPAGE": eval(
                    re.findall('".*?"', re.findall('id="__PREVIOUSPAGE" value=".*?" />', html)[0])[1]),
                "__EVENTVALIDATION": eval(
                    re.findall('".*?"', re.findall('id="__EVENTVALIDATION" value=".*?" />', html)[0])[1]),
                "TextBox1": username,
                "TextBox2": password,
                "RadioButtonList1": "学生",
                "Button4_test": ''
            }

            # 登陆验证
            s = requests.post(url, data=data, headers=header)
            s.raise_for_status()
            s.encoding = s.apparent_encoding
            html2 = s.text
            return {'status': True, 'name': re.findall(str(username) + '.*?同学', html2)[0].split('  ')[1][:-2]} if (
                    str(username) in re.findall('<span id="xhxm">.*?</span>', html2)[0]) else False


        except:
            return False
