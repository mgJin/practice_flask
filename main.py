from flask import Flask, render_template, request
from extractor.indeed import extract_indeed_jobs
from extractor.wwr import extract_wwr_jobs

app = Flask("jobScrapper")


@app.route("/")
def home():
  return render_template("home.html", name="jjjj")


@app.route("/search")
def hello():
  keyword = request.args.get("keyword")  #keyword라는 name으로 이것을 받겠다
  indeed = extract_indeed_jobs(keyword)
  wwr = extract_wwr_jobs(keyword)
  jobs = indeed + wwr

  return render_template("search.html", keyword=keyword, jobs=jobs)


app.run("0.0.0.0")
