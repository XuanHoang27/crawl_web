from __init__ import *
app = Flask(__name__)


@app.route('/',methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route('/redirect',methods=["POST","GET"])
def redirect():
    if request.method == "POST":
        redirect = request.form['select']
        if redirect == "0":
            return render_template("crawl.html")
        if redirect == "1":
            return render_template("classification.html")
        if redirect == "2":
            return render_template("statistic.html")

@app.route('/crawl',methods=["POST","GET"])
def crawl():
    if request.method == "POST":
        mode = request.form['crawl_mode']
        web = request.form['crawl_web']
        main(web, mode)
        return render_template("crawl.html")
    
@app.route('/statistic',methods=["POST","GET"])
def statistic():
    if request.method == "POST":
        statistic_web = request.form['statistic_web']
        statistic_process(statistic_web)
        return render_template("statistic.html")
    
@app.route('/classification',methods=["POST","GET"])
def classification():
    if request.method == "POST":
        classify_web = request.form['classify_web']
        classify_mode = request.form['classify_mode']
        if classify_mode == "detail":
            classify_detail(web=classify_web)
        if classify_mode == "dataonly":
            classify_Non_Detail(web=classify_web)
        return render_template("classification.html", status="Đã phân loại")
    
@app.route('/autoindex_view/')
def autoindex_view(path = "."):
    return AutoIndex(app, browse_root='./static/data').render_autoindex(path)

if __name__ == "__main__":
    app.run()