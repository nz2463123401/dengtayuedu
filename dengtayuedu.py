import time
import httpx
import json


class dengtayude:

    def __init__(self):
        self.task_value = None
        self.quiz_text = None
        self.start_time = None
        self.url = 'https://www.ai-reading.com/index.php'
        self.client = httpx.Client(http2=True, verify=False)
        self.read_time: int = 300  # 阅读时间
        self.r_id: int = 2759  # 文本id
        self.answer = {}
        self.data = {
            'openid': 'XXXXXXXXXXXXXXXXXXXXXXXXX', #opendid
            'sessionKey': 'XXXXXXXXXXXXXXXXXXXXXXXXX' #sessionkey
        }
        self.headers = {
            'Referer': 'https://servicewechat.com/wxb8e4f03655d8c15b/213/page-frame.html',
            'Xweb_xhr': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6763',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh'
        }

    def main(self):
        self.client.get(url=self.url)
        self.get_index21()
        self.get_task_list()
        for i in self.task_value:
            self.r_id = i
            self.get_main()

    def get_main(self):
        self.get_member_info1()
        self.get_text()
        self.get_member_info2()
        self.post_readtime()
        self.get_readtime(type=1)
        self.get_quiz()
        self.post_answer()
        self.get_readtime(type=2)
        self.get_quiz()

    def get_index21(self):
        c = 'lm'
        a = 'index21'
        data = self.data.copy()
        data["topic"] = 'true'
        self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)  # 没啥用，骗一下服务器

    def get_task_list(self):
        c = 'task'
        a = 'myTask'
        data = self.data.copy()
        data["tokentp"] = '2'
        data["type"] = '1'
        data["page"] = '1'
        data["new"] = '1'
        task_list = self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)
        data = json.loads(task_list.text)
        self.task_value = data['data']['task'][0]['task']
        self.task_value = self.task_value.split(",")
        print(self.task_value)

    def get_text(self):
        c = 'lm'
        a = 'request'
        data = self.data.copy()
        data["part"] = '1'
        data["rId"] = str(self.r_id)
        data["n"] = '1'
        self.start_time = int((time.time() - self.read_time) * 1000)
        text = self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)
        print(text.text)

    def post_readtime(self):
        c = 'lm'
        a = 'requestPost'
        data = self.data.copy()
        data["part"] = '1'
        data["rId"] = str(self.r_id)
        data["readTime"] = str(self.read_time)
        data["startTime"] = self.start_time
        data["endTime"] = self.start_time + self.read_time * 1000
        self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)

    def get_readtime(self, type: int):
        c = 'lm'
        a = 'getReadTime'
        data = self.data.copy()
        data["rId"] = str(self.r_id)
        data["readTime"] = str(self.read_time)
        data["type"] = str(type)
        self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)

    def get_quiz(self):
        c = 'lm'
        a = 'request'
        data = self.data.copy()
        data["part"] = "2"
        data["readTime"] = ''
        data["rId"] = str(self.r_id)
        data["review"] = '0'
        self.quiz_text = self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)
        self.get_answer()

    def get_answer(self):
        data = json.load(self.quiz_text)
        quiz_array = data["data"]["quiz"]
        for i in range(len(quiz_array)):
            self.answer['%d' % (i + 1)] = quiz_array[i]["right"]

    def post_answer(self):
        c = 'lm'
        a = 'requestPost'
        data = self.data.copy()
        data["onOption"] = json.dumps(self.answer)
        data["part"] = '2'
        data["readTime"] = str(self.read_time)
        data["endTime"] = str(int(time.time() * 1000))
        data["challenge"] = "undefined"
        data["startTime"] = str(int(time.time() * 1000) - self.read_time * 1000)
        data["rId"] = str(self.r_id)
        self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)

    def get_member_info1(self):
        c = 'lm'
        a = 'getMemberInfo'
        data = self.data.copy()
        self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)

    def get_member_info2(self):
        c = 'lm'
        a = 'getMemberInfo'
        data = self.data.copy()
        data["isGift"] = '1'
        data["tokentp"] = '2'
        self.client.post(url=self.url + '?c=' + c + '&a=' + a, headers=self.headers, data=data)


dengtayude = dengtayude()
dengtayude.main()
