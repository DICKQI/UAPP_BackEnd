from django.test import TestCase
import json, random, requests
# Create your tests here.

class UserViewTest(TestCase):

    def setUp(self) -> None:
        pass

    def testRegester(self):
        times = int(input('输入要注册的数量：'))
        errCounter = 0
        errMsg = []
        for i in range(times):
            password = str(random.randint(10000, 99999))
            email = str(random.randint(1000, 9999)) + '@' + 'qq.com'
            nickname = str(random.randint(100000, 999999))
            school = 'bnuz'

            re = requests.post(
                url='http://127.0.0.1:8000/users/register/',
                json={
                    "password": password,
                    "nickname": nickname,
                    "email": email,
                    "school": school
                }
            )
            if re.status_code != 200:
                errCounter += 1
                errMsg.append({
                    'errMsg': re.content,
                    'password': password,
                    'nickname': nickname,
                    'email': email
                })
            print('status code: ' + str(re.status_code))
        print('error count: ' + str(errCounter))
        if errMsg:
            print(errMsg)