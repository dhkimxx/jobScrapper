import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup


#검색 결과의 개수를 구하는 function
def get_cnt_result(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    cnt_result = int(soup.find("strong",{"class": "dev_tot"}).string.replace(",",""))
    return cnt_result

def extract_job(html):
    title = html.find("a",{"class": "title dev_view"})
    if title:
        title = title["title"]
    else:
        return
    company = html.find("a",{"class": "name dev_view"})["title"]
    condition = html.find("p",{"class":"option"}).get_text(strip=True)
    job_id = html["data-gno"]
    link = f"https://www.jobkorea.co.kr/Recruit/GI_Read/{job_id}"
    return {
        'title': title,
        'company': company,
        'condition': condition,
        'link': link
    }

def extract_jobs(url, last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping JobKorea : page {page+1} / {last_page}")
        result = requests.get(f"{url}&Page_No={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("li", {"class": "list-post"})
        for result in results:
            job = extract_job(result)
            if job:
                jobs.append(job)
    return jobs


def get_jobs(word):
    limit = 20 # 한 페이지에 출력되는 개수
    url = f"https://www.jobkorea.co.kr/Search/?stext={word}"
    cnt_result = get_cnt_result(url)
    last_page = cnt_result // limit + 1
    jobs = extract_jobs(url, last_page)
    return jobs


