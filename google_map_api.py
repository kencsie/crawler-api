# 說明文獻
# https://googlemaps.github.io/google-maps-services-python/docs/
# https://developers.google.com/maps/documentation/places/web-service/search-nearby#maps_http_places_nearbysearch-py
import googlemaps

#注意! 這邊需要用自己的API key
API_KEY = ""

#創建一個文件，用來存放資料
output = open("map data.txt", "w", encoding="UTF-8")

#輸入關鍵詞
key_word = input("請輸入關鍵詞")
#輸入地址
address = input("請輸入地址")

#執行googlemaps套件，並確認地址是合法的
gmaps = googlemaps.Client(key=API_KEY)
try:
      geocode_result = gmaps.geocode(address)
      loc = geocode_result[0]["geometry"]["location"]
      places = gmaps.places_nearby(keyword=key_word, location=loc, radius=2500)
except:
      print("地址有問題喔")
      quit()


#顯示api回傳的全部內容
#print(places, file=output)
#顯示結果到終端機
print("總共有", len(places["results"]), "個地點", sep="")

#整理內容，印出每個結果，並儲存到檔案中
index = 0
while index < len(places["results"]):
    print(places["results"][index]["name"], file=output)
    print("評價:", places["results"][index]["rating"], sep="", file=output)
    print("地址:", places["results"][index]["vicinity"], sep="", file=output)
    print("絕對位置:", places["results"][index]["geometry"]
          ["location"], sep="", file=output)
    print("", file=output)
    index += 1
