import requests
import json
import pandas as pd 
from pandas import DataFrame


def find_detail(get_movieNm, get_directorNm):
    api_key = '38d2c8854e32a32fd76a72ab8d5c7de5'
    url_tpl = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={key}&movieNm={movieNm}&directorNm={directorNm}"
    api_url = url_tpl.format(key=api_key, movieNm=get_movieNm, directorNm=get_directorNm) #반도랑 연상호 부분 parameter로 바꿔야함

    response=requests.get(url=api_url).json()
    
    return response['movieListResult']['movieList']


def find_detail_bycode(detail_code):
    
    api_key = '38d2c8854e32a32fd76a72ab8d5c7de5'
    url_tpl = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movie_code}"
    api_url = url_tpl.format(key=api_key, movie_code=detail_code) #반도랑 연상호 부분 parameter로 바꿔야함
    response=requests.get(url=api_url).json()
    
    return response['movieInfoResult']['movieInfo']

print(find_detail('1987','장준환'))
print(find_detail_bycode('20170590'))