#데이터 분석을 하기위한 라이브러리
import pandas as pd

#웹 크롤링을 할 수 있는 라이브러리
from bs4 import BeautifulSoup

#마찬가지로 웹 크롤링을 도와주는 라이브러리
from urllib.request import Request,urlopen

#웹 크롤링하는거
import requests

#직접 버튼을 누르고 페이지에서 동작을 가능하게 해주는 라이브러리
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


#현재 제품의 별점 1부터 5까지 전부 크롤링하여 저장
def OneToFive(url):


    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.implicitly_wait(10)
    driver.get(url)

    data_5 = None
    data_4 = None
    data_3 = None
    data_2 = None
    data_1 = None

    for i in range(2,7):
        star_path = f"/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[{i}]/a"
        # print(star_path)
        # /html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[2]/a
        # /html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[3]/a
        # /html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[4]/a
        # /html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[5]/a
        # /html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[6]/a
        star_btn = driver.find_element(By.XPATH, star_path)

        action = ActionChains(driver)
        action.move_to_element(star_btn).perform()
        driver.implicitly_wait(10)
        star_btn.click()                
        driver.implicitly_wait(10)

        # #url의 해당 주소의 페이지 가져오기
        # webpage = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})

        webpage = driver.page_source

        # 가져온 HTML를 태그로 분류하기 위해 BeautifulSoup 사용
        soup = BeautifulSoup(webpage, "html.parser")

        # f"<a href="#" role="button" class="" data-nclick="N=a:rev.grd5">"
        review_count_path = f"/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[2]/div[2]/ul/li[{i}]/a/em"

        review_count = driver.find_element(By.XPATH, review_count_path)
        
        count_str = review_count.text

        count_str = count_str.replace(',', '')
        count_str = count_str.replace('(', '')
        count_str = count_str.replace(')', '')

        count = int(count_str)

        repeat = 100 if(count >= 2000) else count//20

        for j in range(1,repeat+1):
            if(j < 10):
                review_list_path = f"/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a[{j}]"
                review_list_path_next = None
                # print(review_list_path)
            elif (j % 10 != 0):
                review_list_path = f"/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a[{j%10 + 1}]"
                review_list_path_next = None
                # print(review_list_path)
            else:
                review_list_path = f"/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a[{10 if(j == 10) else 11}]"
                review_list_path_next = f"/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/div[3]/a[{11 if(j == 10) else 12}]"
                # print(review_list_path)
                # print(review_list_path_next)
            review_list_btn = driver.find_element(By.XPATH, review_list_path)
            review_list_btn.click()

            if(j > 1):
                now_sentence = ""
                while (before_sentence != now_sentence):
                    # 가져온 HTML을 class로 분류하여 댓글만 가져오기
                    webpage_just_str = str(soup.find_all(
                        attrs=('class', 'reviewItems_text__XrSSf')))

                    # 가져온 HTML에서 태그 br, em삭제
                    webpage_del_tag_str_1 = webpage_just_str.replace('<br/>', '')
                    webpage_del_tag_str_2 = webpage_del_tag_str_1.replace('<em>', '')
                    webpage_del_tag_str_3 = webpage_del_tag_str_2.replace('</em>', '')
                    webpage_del_tag_str_4 = webpage_del_tag_str_3.replace('</p>', '')

                    # 분류한 댓글들을 가각 분리하기
                    webpage_each_str = webpage_del_tag_str_4.split(
                        '<p class="reviewItems_text__XrSSf">')

                    # 첫번째 인덱스에 '[' 가 들어가서 지우기
                    webpage_each_str.remove('[')

                    now_sentence = webpage_each_str[0]


            # 가져온 HTML을 class로 분류하여 댓글만 가져오기
            webpage_just_str = str(soup.find_all(
                attrs=('class', 'reviewItems_text__XrSSf')))

            # 가져온 HTML에서 태그 br, em삭제
            webpage_del_tag_str_1 = webpage_just_str.replace('<br/>', '')
            webpage_del_tag_str_2 = webpage_del_tag_str_1.replace('<em>', '')
            webpage_del_tag_str_3 = webpage_del_tag_str_2.replace('</em>', '')
            webpage_del_tag_str_4 = webpage_del_tag_str_3.replace('</p>', '')

            # 분류한 댓글들을 가각 분리하기
            webpage_each_str = webpage_del_tag_str_4.split(
                '<p class="reviewItems_text__XrSSf">')

            # 첫번째 인덱스에 '[' 가 들어가서 지우기
            webpage_each_str.remove('[')

            before_sentence = webpage_each_str[0]

            if(j == 1):
                if i == 2:
                    data_5 = webpage_each_str
                if i == 3:
                    data_4 = webpage_each_str
                if i == 4:
                    data_3 = webpage_each_str
                if i == 5:
                    data_2 = webpage_each_str
                if i == 6:
                    data_1 = webpage_each_str
            else:
                if i == 2:
                    data_5 += webpage_each_str
                if i == 3:
                    data_4 += webpage_each_str
                if i == 4:
                    data_3 += webpage_each_str
                if i == 5:
                    data_2 += webpage_each_str
                if i == 6:
                    data_1 += webpage_each_str
            if(review_list_path_next != None and j != 100):
                review_list_next_btn = driver.find_element(By.XPATH, review_list_path)
                review_list_next_btn.click()

    all_df_dic = {
        '5': data_5,
        '4': data_4,
        '3': data_3,
        '2': data_2,
        '1': data_1
    }

    all_df = pd.DataFrame.from_dict(all_df_dic,orient='index')

    all_df = all_df.transpose()

    return all_df


all_df = OneToFive("https://search.shopping.naver.com/catalog/34563199618?&NaPm=ct%3Dlfx8vxuo%7Cci%3Dc61fb1098b471d88fea549dcd418001208a2a78f%7Ctr%3Dslcc%7Csn%3D95694%7Chk%3D8becaba54daa26c9868980e4c93112f25adb2e38")
print('')