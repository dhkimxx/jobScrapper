import requests
from bs4 import BeautifulSoup
import re #search result 개수를 문자열에서 숫자를 추출하기 위해서 module 사용


#검색 결과의 개수를 구하는 function
def get_cnt_result(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    cnt_result = soup.find("div",{"id": "searchCountPages"})\
        .string.replace(",","")
    result = re.findall("\d+",cnt_result) #숫자 추출 (module 're')
    cnt_result = int(result[1])
    return cnt_result

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None
    condition = html.find("div",{"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title':title,
        'company':company,
        'condition': condition,
        'link': f"https://kr.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(url, last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping indeedKR: page {page+1} / {last_page}")
        result = requests.get(f"{url}&start={page*10}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    limit = 15  # 한 페이지에 출력되는 개수
    url = f"https://kr.indeed.com/jobs?q={word}"
    cnt_result = get_cnt_result(url)
    last_page = cnt_result // limit + 1
    jobs = extract_jobs(url, last_page)
    return jobs