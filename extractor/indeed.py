from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  results = []
  for page in range(pages):

    base_url = "https://kr.indeed.com/jobs"
    final_url = f"https://kr.indeed.com/jobs?q={keyword}&start={page*10}"
    print("Requesting", final_url)
    options = Options()
    
    options.add_argument("--no-sandbox")
    
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    browser.get(final_url)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    print(soup)
    print("soup가 문제인가")
    job_list = soup.find('ul', class_="jobsearch-ResultsList")
    print(job_list)
    
    print("여기?")
    jobs = job_list.find_all('li', recursive=False)
    print(len(jobs))
    print("아닌가?")
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']

        name = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")

        job_data = {
          'link': f"https://kr.indeed.com{link}",
          'company': name.string.replace(",", " "),
          'location': location.string.replace(",", " "),
          'position': title.replace(",", " ")
        }
        results.append(job_data)

  return results


def get_page_count(keyword):

  options = Options()
 
  options.add_argument("--no-sandbox")
  
  options.add_argument("--disable-dev-shm-usage")

  browser = webdriver.Chrome(options=options)
  browser.get(f"https://kr.indeed.com/jobs?q={keyword}")
  soup = BeautifulSoup(browser.page_source, 'html.parser')

  pagination = soup.find('nav', role="navigation")
  if pagination == None:
    return 1  #None이라면 우리가 스크랩할 페이지는 1개라는 뜻

  pages = pagination.find_all('div', recursive=False)
  count = len(pages)
  if count >= 5:
    return 5  #5페이지 이상이라도 우리는 5페이지만 스크랩할 것
  else:
    return count
