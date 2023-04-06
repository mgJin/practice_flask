from flask import Flask, render_template, request, redirect, send_file
from extractor.indeed import extract_indeed_jobs
from extractor.wwr import extract_wwr_jobs
from file import save_to_file

db = {}

app = Flask("jobScrapper")


@app.route("/")
def home():
  return render_template("home.html", name="jjjj")


@app.route("/search")
def hello():
  keyword = request.args.get("keyword")  #keyword라는 name으로 이것을 받겠다
  if keyword == None:
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
  else:
    indeed = extract_indeed_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = indeed + wwr
    db[keyword] = jobs

  return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)


#savetofile로 파일을 만든다
#send_file에는 파일이름이 필요, 뒤에것은 다운로드가 되게 하는것
app.run("0.0.0.0")
