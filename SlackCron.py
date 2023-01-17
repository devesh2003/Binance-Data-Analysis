import requests
'''
curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}'
https://hooks.slack.com/services/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
'''

data = {
    "Time":  "2021-04-01 00:00:00",
    "Close Price": "1231",
    "Volume": "123123",
    "Signal": "Buy",
    "Target": "21321",
    "Stop Loss": "3131"
}

class SlackCron:
    def __init__(self):
        self.url = "https://hooks.slack.com/services/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"
        self.data = {}
        self.message = "--------\n"
    
    def send(self,data):
        self.data = data
        for key in self.data:
            self.message += f"{key}: {self.data[key]}\n"
        self.message += "--------\n"
        r = requests.post(self.url, json={"text":self.message},verify=False)