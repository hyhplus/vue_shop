# coding:utf-8 
# author: Evan
# datetime: 18-9-17 下午11:10

import requests
import json


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【云片网】您的验证码是{code}".format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        # print(re_dict)
        return re_dict


# if __name__ == "__main__":
#     yun_pian = YunPian("c034bd24302cd03158e0e35bed50adf1")
#     yun_pian.send_sms("2018", "153****4026")
