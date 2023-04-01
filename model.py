#데이터 분석을 하기위한 라이브러리
import pandas as pd
#웹 크롤링을 할 수 있는 라이브러리
from bs4 import BeautifulSoup
#마찬가지로 웹 크롤링을 도와주는 라이브러리
from urllib.request import Request,urlopen
#웹 크롤링하는거
import requests
#크롤링 할 주소
url = "https://search.shopping.naver.com/catalog/34563199618?&NaPm=ct%3Dlfx8vxuo%7Cci%3Dc61fb1098b471d88fea549dcd418001208a2a78f%7Ctr%3Dslcc%7Csn%3D95694%7Chk%3D8becaba54daa26c9868980e4c93112f25adb2e38"
#url의 해당 주소의 페이지 가져오기
webpage = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
#가져온 HTML를 태그로 분류하기 위해 BeautifulSoup 사용
soup = BeautifulSoup(webpage.content,"html.parser")
#가져온 HTML을 class로 분류하여 댓글만 가져오기 
webpage_str = str(soup.find_all(attrs=('class','reviewItems_text__XrSSf')))
#분류한 댓글들을 가각 분리하기
webpage_str = webpage_str.split('<p class="reviewItems_text__XrSSf">')
#출력
for w_str in webpage_str:
    print(w_str+"\n\n\n\n\n")