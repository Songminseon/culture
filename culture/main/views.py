from django.shortcuts import render, redirect
from content.models import Content, Content_other
from django.db.models import Q
import requests
import json
from lxml.html import parse
from io import StringIO
import os, sys
from PIL import Image

global grade

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

def find_imgsrc(movieName,category):
    base_url = 'https://www.google.co.kr/search?q={movieNm}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwic-taB9IXVAhWDHpQKHXOjC14Q_AUIBigB&biw=1842&bih=990' 
    url = base_url.format(movieNm=category+movieName+"포스터")

    # html 소스 가져오기
    text = requests.get(url).text

    # html 문서로 파싱
    text_source = StringIO(text)
    parsed = parse(text_source)
    doc = parsed.getroot()
    imgs = doc.findall('.//img')

    img_list = []   # 이미지 경로가 담길 list
    for link in imgs:
        img_list.append(link.get('src'))

    return img_list[1]



def main(request):
    content = Content.objects
    return render(request, 'main.html', {"content":content})

def result(request):
    if request.method == "POST":   #중복체크 안되도록 구현
        aws1 = request.POST.get('answer1')
        aws2 = request.POST.get('answer2')
        aws3 = request.POST.get('answer3')
        aws4 = request.POST.get('answer4')
        aws5 = request.POST.get('answer5')
        grade = 0
        history_list = []
        recommend_list = []
        movieNm_list = []
        theater_list = []
        musical_list = []
        directorNm_list = []
        detail_list = []
        detail_code = []
        info_dict = {}
        img_list = []
        detail_theater = []
        detail_musical = []
        if aws1 == 'user1_choice1':
            grade = grade+1
        else:
            history_list.append('518민주화운동')
        if aws2 == "user2_choice1":
            grade = grade+1
        else:
            history_list.append('광해')
        if aws3 == "user3_choice2":
            grade = grade + 1
        else:
            history_list.append('병자호란')
        if aws4 == "user4_choice1":
            grade = grade + 1
        else:
            history_list.append('황산벌 전투')
        if aws5 == "user5_choice1":
            grade = grade + 1
        else:
            history_list.append('안중근')


        #############추천목록 구현#################
        if len(history_list) == 0:
            recommend_list = "참잘했어요"
        else:
            for i in history_list:
                recommend_list.extend(Content.objects.filter(history=i))
                movieNm_list.extend(Content.objects.filter(Q(history=i) & Q(category="영화")).values('name')) #detail정보 찾을때
                directorNm_list.extend(Content.objects.filter(Q(history=i) & Q(category="영화")).values('directorNm'))  #detail정보 찾을때

        ##api 정보 가져오기##
        for i in range(0, len(movieNm_list)):
            detail_code.append(find_detail(movieNm_list[i]['name'],directorNm_list[i]['directorNm'])[0]['movieCd'])
            img_src =  find_imgsrc(movieNm_list[i]['name'],"영화")
            ## detail_list.extend(find_detail(movieNm_list[i]['name'],directorNm_list[i]['directorNm'])) 
            
            # detail_list.append(img_src)
            detail_information = find_detail_bycode(detail_code[i])
            movieNm = detail_information['movieNm']
            movieNmEn = detail_information['movieNmEn']
            showTm = detail_information['showTm']
            directorNm = detail_information['directors'][0]['peopleNm']
            ##추가해야할 요소
            genreNm = detail_information['genres'][0]['genreNm']
            actor_name = detail_information['actors'][0]['peopleNm'] + detail_information['actors'][1]['peopleNm'] + detail_information['actors'][2]['peopleNm']
            watchGradeNm = detail_information['audits'][0]['watchGradeNm']

            detail_list.append([{'movieNm':movieNm, 'movieNmEn':movieNmEn, 'showTm':showTm, 'directorNm':directorNm, 'img_src':img_src, 'genreNm':genreNm, 'actor_name':actor_name, 'watchGradeNm':watchGradeNm}])
            # detail_list.append(find_detail_bycode(detail_code[i]))
            
        for i in history_list:
            theater_list.extend(Content.objects.filter(Q(history=i) & Q(category="연극")).values('name'))
            musical_list.extend(Content.objects.filter(Q(history=i) & Q(category="뮤지컬")).values('name'))

        for i in range(0, len(theater_list)):
            info_query = Content_other.objects.filter(title=str(theater_list[i]['name'])).values()
            info_title = info_query[0]['title']
            info_description = info_query[0]['description']
            img_src = find_imgsrc(theater_list[i]['name'],"연극")
            detail_theater.append([{'title':info_title, 'description':info_description, 'img_src':img_src}])

        for i in range(0, len(musical_list)):
            info_query = Content_other.objects.filter(title=str(theater_list[i]['name'])).values()
            info_title = info_query[0]['title']
            info_description = info_query[0]['description']
            img_src = find_imgsrc(theater_list[i]['name'],"뮤지컬")
            detail_musical.append([{'title':info_title, 'description':info_description, 'img_src':img_src}])


        info1 = {'grade':grade, 'detail_list':detail_list, 'detail_theater':detail_theater, 'detail_musical':detail_musical}       
        info_dict.update(info1)
        return render(request, 'result.html', info_dict)
    else:
        return render(request,'test.html')

    return redirect('test')





def recommend(request):
    if request.method == "POST":
        history_list = []
        category_list = []
        choice1 = request.POST.getlist('user_choice')
        choice2 = request.POST.get('user_choice2')
        for i in choice1:
            if i == 'history1':
                history_list.append('518민주화운동')
            elif i == 'history2':
                history_list.append('을미사변')
            elif i == 'history3':
                history_list.append('삼국시대')
            elif i == 'history4':
                history_list.append('인천상륙작전')
            elif i == 'history5':
                history_list.append('625전쟁')
            else:
                history_list.append('임진왜란')

        
        if choice2 == 'category1':
            category_user='영화'
        elif choice2 == 'category2':
            category_user = '연극'
        else:
            category_user = '뮤지컬'
        
        recommend_list = []
        directorNm_list = []
        detail_list = []
        detail_code = []


        for i in history_list:
            recommend_list.extend(Content.objects.filter(Q(category=category_user) & Q(history=i)).values('name')) #카테고리와 역사에 따른 분류
        
        if category_user=="영화":
            for i in range(0,len(recommend_list)):
                directorNm_list.extend(Content.objects.filter(Q(name=recommend_list[i]['name']) & Q(category="영화")).values('directorNm'))          
            
            for i in range(0, len(recommend_list)):
                detail_code.append(find_detail(recommend_list[i]['name'],directorNm_list[i]['directorNm'])[0]['movieCd'])
                img_src =  find_imgsrc(recommend_list[i]['name'],"영화")
             
                detail_information = find_detail_bycode(detail_code[i])
                movieNm = detail_information['movieNm']
                movieNmEn = detail_information['movieNmEn']
                showTm = detail_information['showTm']
                directorNm = detail_information['directors'][0]['peopleNm']
                genreNm = detail_information['genres'][0]['genreNm']
                actor_name = detail_information['actors'][0]['peopleNm'] + detail_information['actors'][1]['peopleNm'] + detail_information['actors'][2]['peopleNm']
                watchGradeNm = detail_information['audits'][0]['watchGradeNm']

                detail_list.append([{'movieNm':movieNm, 'movieNmEn':movieNmEn, 'showTm':showTm, 'directorNm':directorNm, 'img_src':img_src, 'genreNm':genreNm, 'actor_name':actor_name, 'watchGradeNm':watchGradeNm}])
        
        else: 
            for i in range(0, len(recommend_list)):
                info_query = Content_other.objects.filter(title=str(recommend_list[i]['name'])).values()
                info_title = info_query[0]['title']
                info_description = info_query[0]['description']
                if category_user=="연극":
                    img_src = find_imgsrc(recommend_list[i]['name'],"연극")
                else: #뮤지컬인 경우
                    img_src = find_imgsrc(recommend_list[i]['name'],"뮤지컬")
                    
                detail_list.append([{'title':info_title, 'description':info_description, 'img_src':img_src}])

                
      


        context =  {'recommend':recommend_list,'detail_list':detail_list, 'test':recommend_list, 'category':category_user}
        return render(request, 'recommend.html', context)
    else:
        return render(request, 'recommend.html')
    return redirect('recommend')


def home(request):
    return render(request, 'home.html')

def test(request):
    return render(request, 'test.html')
