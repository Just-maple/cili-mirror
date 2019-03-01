#!/usr/bin/env python3
import requests
import re
from flask import Flask, request, abort, Response, session
import json, os, inspect, datetime, random

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]


class WebServer(object):
    def __init__(self):
        self.server = Flask(__name__)
        self.reigsterApiRouter()
        self.getRouter = {}
        self.postRouter = {}

    def reigsterRoute(self, apiAddr, methods, api):
        app = self.server

        @app.route(apiAddr, methods=methods)
        def apiMethod(**kwargs):
            args = request.args
            json = request.json
            ip = request.headers.get("X-Real-IP")
            kwargs["args"] = args or {}
            kwargs["ip"] = ip or ""
            kwargs["json"] = json or {}
            user_id = session.get("user")
            return api(**kwargs)

    def reigsterApiRouter(self):
        self.reigsterRoute("/api/<api>", ["GET", "POST"], self.apiRouter)

    def registerGetApi(self, route, methods):
        self.getRouter[route] = methods

    def registerPostApi(self, route, methods):
        self.postRouter[route] = methods

    def apiRouter(self, api, **kwargs):
        apiMethod = None
        if request.method == "GET":
            apiMethod = self.getRouter.get(api)
        elif request.method == "POST":
            apiMethod = self.postRouter.get(api)
        else:
            abort(500)
            return
        if apiMethod:
            return self.renderJSONResponse(apiMethod, kwargs)
        else:
            abort(500)
            return

    def renderJSONResponse(self, apiMethod, kwargs):
        res = {}
        res['ok'] = False
        res['data'] = None
        code = 200
        try:
            apiArg = {}
            args = inspect.getargspec(apiMethod).args
            for arg in args:
                if arg == 'self':
                    continue
                apiArg[arg] = kwargs.get(arg)
            res['data'] = apiMethod(**apiArg)
            res['ok'] = True
        except UserWarning as msg:
            error = str(msg)
            res['err'] = error
            print(error)
            code = 500
        return Response(
            status=code, response=json.dumps(res, ensure_ascii=False))

    def runDebug(self, port):
        self.server.run(host="0.0.0.0", port=port, debug=True)

    def run(self, port):
        from gevent import pywsgi
        pywsgi.WSGIServer(('0.0.0.0', port), self.server).serve_forever()

    def raiseError(self, errorMsg):
        raise (UserWarning(errorMsg))


class cilidaquan(object):
    url = 'http://cilidaquan.biz/cldq/{key}/{page}-0-{ftype}.html'

    ftype = {
        "all": 0,
        "video": 2,
    }

    def __init__(self):
        pass

    def seach(self, key, ftype='all', page=1):
        url = self.url.format(key=key, ftype=self.ftype[ftype], page=page)
        headers = {'User-Agent': random.choice(user_agent)}
        res = requests.get(url, headers=headers)
        res.encoding = 'utf8'
        html_text = res.text
        # print(re.findall(r'<dd .+?</dd>',html_text)[1])
        print(html_text)
        total = re.findall(r'搜索到(.+?)个磁力链接', html_text)
        if not (len(total)):
            print(html_text)
            raise (EnvironmentError)
        total = total[0]
        details = (re.findall(
            r'target=\'_blank\'>([^\t]+?)</a></dt>.+?<dd .+?收录时间:<b>(.+?)</b>.+?文件大小:<b>(.+?)</b>.+?文件数:<b>(.+?)</b>.+?href=\'/magnet/(.+?)\.html#.+?<span class=\'name\'>(.+?)</span>.+?</dd>',
            html_text, re.S))
        temp = ['title', 't_create', 'size', 'files_cnt', 'magnet']
        l = len(temp)
        data = []
        for d in details:
            res = {}
            for i in range(l):
                res[temp[i]] = d[i]
            data.append(res)
        return {"magnets": data, "total": total}


class CiliServer(WebServer):
    cili = cilidaquan()

    def GetCili(self, args):
        page = args.get("page", 1)
        ftype = args.get("ftype", 'all')
        key = args.get("key", '')
        if key:
            return self.cili.seach(key, ftype, page)

    def initRoute(self):
        self.registerGetApi("key", self.GetCili)


if __name__ == "__main__":
    server = CiliServer()
    server.initRoute()
    server.runDebug(9299)