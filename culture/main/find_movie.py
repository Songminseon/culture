import requests
import json
import pandas as pd 
from pandas import DataFrame


api_key = '38d2c8854e32a32fd76a72ab8d5c7de5'
url_tpl = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={key}&movieNm={movieNm}&directorNm={directorNm}"
api_url = url_tpl.format(key=api_key, movieNm="반도", directorNm="연상호") #반도랑 연상호 부분 parameter로 바꿔야함

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
session = requests.Session()
session.headers.update({'User-agent': user_agent, 'refer':None})

r = session.get(api_url)
r.encoding = "utf-8"
print(r.text)


# print(find_detail("반도", "연상호")["movieListResult"]["totCnt"])
##영화코드따서 detail information 딸수도 있음<response>
