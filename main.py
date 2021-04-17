from flask import  Flask, render_template, request, redirect, send_file
from saramin import get_jobs as get_si_jobs
from jobkorea import get_jobs as get_jk_jobs
from indeedkr import get_jobs as get_ind_kr_jobs
from incruit import  get_jobs as get_incrt_jobs
from career import get_jobs as get_crr_jobs
from exporter import save_to_file

app = Flask("KoreanJobScrapper")

db = {}

@app.route('/')
def home():
    return render_template("templates.html")

@app.route("/report")
def report():
    SearchingSite = request.args.get('SearchingSite')
    word = request.args.get('word')
    if word:
        word = word.lower()
        db_word = SearchingSite + word
        existJobs = db.get(db_word)
        if existJobs:
            jobs = existJobs
        else:
            if SearchingSite == "jk":
                jobs = get_jk_jobs(word)
                db[db_word] = jobs
            elif SearchingSite == "si":
                jobs = get_si_jobs(word)
                db[db_word] = jobs
            elif SearchingSite == "ind_kr":
                jobs = get_ind_kr_jobs(word)
                db[db_word] = jobs
            elif SearchingSite == "incrt":
                jobs = get_incrt_jobs(word)
                db[db_word] = jobs
            elif SearchingSite == "crr":
                jobs = get_crr_jobs(word)
                db[db_word] = jobs
            else:
                return redirect('/')
    else:
        return redirect('/')
    return render_template(
        "report.html",
        resultsNumber = len(jobs),
        searchingBy = word,
        jobs = jobs
    )

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect('/')
