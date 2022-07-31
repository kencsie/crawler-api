from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup


def board_name(in_url, in_headers):
    req = Request(url=in_url, headers=in_headers)
    html = urlopen(req).read()
    bs = BeautifulSoup(html, "html.parser")

    data_set = bs.findAll("div", "board-name")
    print(data_set)

    out = open("billboard_list.txt", "w", encoding="UTF-8")
    for iter in data_set:
        print(iter.get_text(), file=out)


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) \
Gecko/20100101 Firefox/23.0"}
url = "https://www.ptt.cc/bbs/index.html"

board_name(url, headers)
