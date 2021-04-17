import requests
from bs4 import BeautifulSoup
import re #search result 개수를 문자열에서 숫자를 추출하기 위해서 module 사용


#검색 결과의 개수를 구하는 function
def get_cnt_result(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    cnt_result = soup.find("span",{"class": "numall"}).string
    result = re.findall("\d+",cnt_result) #숫자 추출 (module 're')
    cnt_result = int(result[0])
    return cnt_result

def extract_job(html):
    title = html.find("span", {"class": "rcrtTitle"})
    if title:
        link = title.find("a")["href"].replace("*search","")
        title = title.get_text()
    else:
        return
    company = html.find("h3").get_text()
    if company:
        company = company.replace("관심기업등록","")
    condition = html.find("p",{"class": "etc"}).get_text()
    return {
        'title':title,
        'company':company,
        'condition': condition,
        'link': link
    }

def extract_jobs(url, last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping incruit: page {page+1} / {last_page}")
        result = requests.get(f"{url}&startno={page*20}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("li")
        for result in results:
            job = extract_job(result)
            if job:
                jobs.append(job)
    return jobs

def get_jobs(word):
    limit = 20  # 한 페이지에 출력되는 개수
    url = f"https://search.incruit.com/list/search.asp?col=job&il=y&kw={word}"
    cnt_result = get_cnt_result(url)
    last_page = cnt_result // limit + 1
    jobs = extract_jobs(url, last_page)
    return jobs