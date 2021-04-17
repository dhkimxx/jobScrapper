import requests
from bs4 import BeautifulSoup
import re #search result 개수를 문자열에서 숫자를 추출하기 위해서 module 사용


#검색 결과의 개수를 구하는 function
def get_cnt_result(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    cnt_result = soup.find("span",{"class": "cnt_result"})\
        .string.replace(",","")
    result = re.findall("\d+",cnt_result) #숫자 추출 (module 're')
    cnt_result = int(result[0])
    return cnt_result

def extract_job(html):
    title = html.find("h2",{"class": "job_tit"}).find("a")["title"]
    company = html.find("strong",{"class": "corp_name"}).find("a")["title"]
    condition = html.find("div",{"job_condition"}).get_text(strip=True)
    job_id = html["value"]
    link = f"https://www.saramin.co.kr/zf_user/jobs/relay/view?&rec_idx={job_id}"
    return {
        'title': title,
        'company': company,
        'condition': condition,
        'link': link
    }

def extract_jobs(url, last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Saramin : page {page+1} / {last_page}")
        result = requests.get(f"{url}&recruitPage={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    limit = 40 # 한 페이지에 출력되는 개수
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?&searchword={word}&recruitPageCount={limit}"
    cnt_result = get_cnt_result(url)
    last_page = cnt_result // limit + 1
    jobs = extract_jobs(url, last_page)
    return jobs


