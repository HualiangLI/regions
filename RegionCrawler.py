#coding=utf-8
import re
import json

import sys
version = sys.version_info
major_version = version[0]
if major_version == 3:
    from urllib import request
    urlopen = request.urlopen
    Request = request.Request
elif major_version == 2:
    from urllib2 import urlopen
    from urllib2 import Request


def __crawler__():
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    req = Request("http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/201703/t20170310_1471429.html",
                  headers=headers)
    r = urlopen(req)
    return r.read().decode('utf-8')


def __process__(text):
    matched_obj = re.findall(r'<p class="MsoNormal">.*?</p>', text, re.M | re.I)

    data = {
        'province': [],
        'city': [],
        'district': []
    }
    for html in matched_obj:
        print(html)
        searched_obj = re.search(r'<span lang="EN-US">(\d+)<span>.*?<span style="font-family: .*?">\s*(\w+)</span>',
                                 html, re.M | re.I)
        if searched_obj:
            result_l = searched_obj.groups()
            if result_l and len(result_l) == 2:
                region_id, region_name = result_l
                code = int(region_id)
                if code % 10000 == 0:
                    data['province'].append({'code': region_id, 'name': region_name})
                elif code % 100 == 0:
                    data['city'].append({'code': region_id, 'name': region_name})
                else:
                    data['district'].append({'code': region_id, 'name': region_name})
    return data


class RegionCrawler(object):
    def __init__(self):
        self._region_data = __process__(__crawler__())

    @property
    def data(self):
        return self._region_data

    def to_json(self):
        return json.dumps(self.data)


if __name__ == '__main__':
    print(RegionCrawler().data)
