# 403 Forbidden解決方法
# https://blog.csdn.net/eric_sunah/article/details/11301873
# try and except
# https://steam.oxxostudio.tw/category/python/basic/try-except.html
# https://stackoverflow.com/questions/3642080/using-python-with-statement-with-try-except-block
# create directory
# https://www.geeksforgeeks.org/create-a-directory-in-python/
# 創建目錄迴避非法字元
# https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
# 只擷取文字內容
# https://stackoverflow.com/questions/40789117/extract-only-text-from-div-tags-on-a-page-using-python-and-beautiful-soup
# UnicodeEncodeError cp950 問題
# https://weirenxue.github.io/2021/06/12/python_cp950_codec_cant_encode/
# 動態決定程式執行位置
# https://stackoverflow.com/questions/38412495/difference-between-os-path-dirnameos-path-abspath-file-and-os-path-dirnam
# 終結程式方法
# https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
# 八卦版的cookie問題
# https://medium.com/誤闖數據叢林的商管人zino/cookic-突破ptt-八卦版十八禁限制-網路爬蟲系列-含影片與程式碼-5f4615031d4b
# Remote end closed connection without response 的解決方法與User-Agent文件
# https://blog.csdn.net/ztf312/article/details/87919027
# https://gist.github.com/pzb/b4b6f57144aea7827ae4

from urllib.request import urlopen
from urllib.request import Request
from random import randint
from bs4 import BeautifulSoup
import os


def find_previous_website(in_url, in_headers):
    #請求網頁
    req = Request(url=in_url, headers=in_headers)
    html = urlopen(req).read()
    bs = BeautifulSoup(html, "html.parser")

    #尋找前一頁的網址
    search_bar = bs.find("div", "action-bar")
    prev_url = search_bar.find_all("a")[3]["href"]
    return "https://www.ptt.cc/" + prev_url


def crawl_website_title(bs):
    return_list = []
    counter = 0
    final_counter = 0
    
    #查找兩種atteributes
    main_page = bs.find_all('div', {'class': ["r-ent", "r-list-sep"]})
    # 從後往前查找
    for element in reversed(main_page):
        # 設定計數器把置底文章排除
        if element.get("class") == ["r-list-sep"]:
            final_counter = counter
            continue
        else:
            counter += 1

        try:
            vote = element.find("span", "hl f3")
            title = element.find("div", "title").get_text()
            hyperlink = "https://www.ptt.cc" + element.find("a").get("href")
            name = element.find("div", "author").get_text()
            date = element.find("div", "date").get_text()
        except: # 如果有遇到文章被刪除的情況
            vote = None
            title = "\n該文章已被刪除\n"
            hyperlink = ""
            name = '-'
            date = element.find("div", "date").get_text()

        # 文章尚未有人發表評論的情形
        if vote is None:
            vote = 0
        else:
            vote = vote.get_text()

        buf = [vote, title[1:-1], hyperlink, name, date]
        return_list.append(buf)

    return return_list[final_counter:]


def crawl_website(in_url, in_headers, billboard_dir):
    #開始請求標題
    req = Request(url=in_url, headers=in_headers)
    html = urlopen(req).read()
    bs = BeautifulSoup(html, "html.parser")

    data_set = crawl_website_title(bs)
    # list 預設格式為 vote/title/href/name/date
    for ele in data_set:
        #把日期分開，以避免非法字元(7/15 -> 715)
        split_date = ele[4][1:].split("/")
        dir = billboard_dir + "\\" + split_date[0] + split_date[1]
        try:
            #創建目錄
            os.mkdir(dir)
        except:
            #print("此日期已創建，繼續...")
            pass

        #把標題中的非法字元移除
        for ch in '\\/:*?"<>|':
            ele[1] = ele[1].replace(ch, '')

        #將標題儲存在檔案內 
        out = open(dir+"\\"+ele[1]+".txt", "w", encoding="UTF-8")
        print("Vote:", ele[0], file=out, sep="")
        print("Title:", ele[1], file=out, sep="")
        print("Hyperlink:", ele[2], file=out, sep="")
        print("Author:", ele[3], file=out, sep="")
        print("Date:", ele[4][1:], file=out, sep="")
        print("\n", file=out)

        #開始請求內容
        try:
            req2 = Request(url=ele[2], headers=in_headers)
            html2 = urlopen(req2).read()
            bs2 = BeautifulSoup(html2, "html.parser")
            page_data = bs2.find("div", "bbs-screen bbs-content").text
            print(page_data, file=out)
        except:
            #print("此文章不存在，繼續...")
            pass


# 程式目前執行的位置
program_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
# 存儲資料的目錄
craw_data_path = program_path + "Data\\"

# 讀取看板內容
billboard_type = []
try:
    file_input = open(program_path + "billboard_list.txt", "r", encoding="UTF-8")
    for line in file_input:
        billboard_type.append(line.rstrip('\n'))
except:
    print("看板文件找不到，請先下載後放置與程式相同資料夾內")
    os._exit(0)
finally:
    file_input.close()

# 填入抓取看板
counter = 1
for item in billboard_type:
    print(counter, ":", item, sep="")
    counter += 1
option = input("請選擇想要爬取的看板.\n(以數字選擇)\n")

try:
    url = "http://www.ptt.cc/bbs/" + billboard_type[int(option)-1] + "/index.html"
except:
    # 超過index的數量
    print("此看板不存在")
    os._exit(0)

# 創建存儲資料目錄
try:
    os.mkdir(craw_data_path)
except:
    print("存儲資料目錄已創建，繼續...")

# 創建該看板目錄
billboard_dir = craw_data_path + billboard_type[int(option)-1]
try:
    os.mkdir(billboard_dir)
except:
    print(billboard_type[int(option)-1],"看板已創建，繼續...", sep="")

# 填入抓取頁數
page = input("請選擇爬取頁數.\n請適度擷取,避免造成站方負擔\n")

# 讀取User-Agent文件
USER_AGENTS = []
try:
    file_input = open(program_path + "user_agent_list.txt", "r", encoding="UTF-8")
    for line in file_input:
        USER_AGENTS.append(line.rstrip("\n"))
except:
    print("User-Agent文件找不到，請先下載後放置與程式相同資料夾內")
    os._exit(0)
finally:
    file_input.close()

for i in range(int(page)):
    # 每次都會更新User-Agent，避免被判定非法存取
    headers = {"User-Agent": USER_AGENTS[randint(0, len(USER_AGENTS)-1)] , "cookie": "over18=1"}
    # 開始執行爬蟲
    crawl_website(url, headers, billboard_dir)
    # 替代上一頁的url
    url = find_previous_website(url, headers)
