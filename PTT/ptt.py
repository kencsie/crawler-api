#region 爬蟲部分
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
#endregion
#region Python 部分
# class 的簡單介紹
# https://www.learncodewithmike.com/2020/01/python-class.html
# public & protected & private
# https://www.tutorialsteacher.com/python/public-private-protected-modifiers
#endregion
#region Python 檔案管理部分
# 不同作業系統路徑的不同
# https://stackoverflow.com/questions/1589930
# 檢查目錄存在
# https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists-2/
# 目錄接合
# https://www.geeksforgeeks.org/python-os-path-join-method/
#endregion

from urllib.request import urlopen
from urllib.request import Request
from random import randint
from bs4 import BeautifulSoup
import os

class crawler_ptt:
    def __init__(self):
        print("歡迎來到PTT爬蟲系統, 開始初始化")
        
        try:
            # 1-1.讀取並印出看板內容
            file_input = open(os.path.join(self.__path, "billboard_list.txt"), "r", encoding="UTF-8")
            counter = 1
            print("以下為各個看板")
            for line in file_input:
                self.__billboard_type.append(line.rstrip('\n'))
                print(counter, ":", line, sep="", end="")
                counter += 1

            # 1-2.選取看板內容
            option = input("請選擇想要爬取的看板.\n(以數字選擇)\n")
            self.__craw_url = "http://www.ptt.cc/bbs/" + self.__billboard_type[int(option)-1] + "/index.html"
        
        except FileNotFoundError:
            print("看板文件找不到，請先下載後放置與程式相同資料夾內")
            os._exit(0)
        except IndexError:
            print("此看板不存在")
            os._exit(0)
        finally:
            file_input.close()


        try:
            #2-1.創建資料目錄
            os.mkdir(self.__data_path)
        except FileExistsError:
            print("存儲資料目錄已創建，繼續...")
        
        try:
            #2-2.創建看板目錄
            self.__board_path = os.path.join(self.__data_path, self.__billboard_type[int(option)-1])
            os.mkdir(self.__board_path)
        except FileExistsError:
            print(self.__billboard_type[int(option)-1],"看板已創建，繼續...", sep="")
        
        # 3.讀取並存入User-Agent文件
        try:
            file_input = open(os.path.join(self.__path, "user_agent_list.txt"), "r", encoding="UTF-8")
            for line in file_input:
                self.__USER_AGENTS.append(line.rstrip("\n"))
        except FileNotFoundError:
            print("User-Agent文件找不到, 請先下載後放置與程式相同資料夾內")
            os._exit(0)
        finally:
            file_input.close()


        # 4.填入抓取頁數
        self.__page = input("請選擇爬取頁數.\n請適度擷取,避免造成站方負擔\n")
        
    def craw(self):
        for i in range(int(self.__page)):
            # 每次都會更新User-Agent，避免被判定非法存取
            headers = {"User-Agent": self.__USER_AGENTS[randint(0, len(self.__USER_AGENTS)-1)] , "cookie": "over18=1"}
            # 開始執行爬蟲
            crawl_website(self.__craw_url, headers, self.__board_path)
            # 替代上一頁的url
            self.__craw_url = find_previous_website(self.__craw_url, headers)
            print("已爬取第", i+1, "頁", sep="")


    # 程式目前執行的位置
    __path = os.path.dirname(os.path.abspath(__file__))
    # 存儲資料的目錄
    __data_path = os.path.join(__path, "Data")
    # 爬取看板目錄
    __board_path = ""
    # 爬取頁數
    __page = 0
    # 爬取的網頁
    __craw_url = ""
    # User_agent 的 list
    __USER_AGENTS = []
    # 看板的 list
    __billboard_type = []


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
        dir = os.path.join(billboard_dir, split_date[0] + split_date[1])
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
        out = open(os.path.join(dir, ele[1]+".txt"), "w", encoding="UTF-8")
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


ptt = crawler_ptt()
ptt.craw()
