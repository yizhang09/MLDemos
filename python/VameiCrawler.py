#-*- coding: UTF-8 -*-
# By Vamei
# scrape the cnblogs

import requests
import BeautifulSoup

import re
import json
from datetime import datetime

def read_page(url, method="get"):
    '''
    read the html page via the URL
    '''
    
    status_code = 0
    while status_code != 200:
        if method == "get":
            r = requests.get(url)
        elif method == "post":
            r = requests.post(url)
        status_code = r.status_code
        print status_code
    page = r.content
    return page

def parse_person_profile(relative, info={}):
    '''
    retrieve the information from the personal profile page
    '''

    r = read_page("http://home.cnblogs.com/u%s" % relative)
    soup  = BeautifulSoup.BeautifulSoup(r)

    # the count of the followers
    el            = soup.find("a", {'id':"follower_count"})
    info['粉丝数']   =  int(el.getText())

    # the time of the registration
    el       = soup.find("div", {'id': "ctl00_cphMain_panel_profile"})
    profile  =  el.ul
    reg_time =  el.ul.findChildren()[0]
    raw = reg_time.getText()
    m   = re.findall("(\d+)", raw)
    m   =  map(int, m)
    dt  = datetime(year=m[0], month=m[1], day=m[2])
    info['开博时间'] = dt.strftime("%Y%m%d")
    return info

def cnblogs_recommend_150():
    '''
    workhouse
    '''
    url = "http://www.cnblogs.com/aggsite/ExpertBlogs"
    r = read_page(url, method="post")
    soup = BeautifulSoup.BeautifulSoup(r)

    # retrieve the information blogger by blogger
    info = []
    anchors = soup.findAll('a')
    # blogger by blogger
    for i, a in enumerate(anchors):
        name = a.getText()
        p_info = {'昵称': name, '排名': i + 1}
        # parse_person_main(a['href'], p_info)
        parse_person_profile(a['href'], p_info)

        info.append(p_info)

    # write the retrieved data into the file
    with open("info", "w") as f:
        rlt = json.dumps(info, indent=4, encoding="UTF-8", ensure_ascii=False)
        f.write(rlt.encode("utf8"))
    return info

if __name__ == "__main__":
    info = cnblogs_recommend_150()
