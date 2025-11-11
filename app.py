from flask import Flask, render_template, request
from fetcher import fetch_html, parse
from collections import defaultdict

app = Flask(__name__)
cache = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        roll_start = int(request.form["roll_start"])
        reg_start = int(request.form["reg_start"])
        count = int(request.form["count"])

        results = []

        for i in range(count):
            roll = roll_start + i
            reg  = reg_start + i
            html = fetch_html(roll, reg)

            if not html or "Candidate Name" not in html:
                results.append({
                    "roll": roll, "reg": reg, "name": "Not Found",
                    "marks": "-", "percent": "-", "status": "Not Found"
                })
                continue

            data = parse(html)
            cache[roll] = data
            status = "PASS" if data["supplementary"] == "" else "SUPP"

            results.append({
                "roll": data["roll"],
                "reg": data["reg"],
                "name": data["name"],
                "marks": data["total_marks"],
                "percent": data["percentage"],
                "status": status,
                "subjects": data["subjects"]
            })

        topper = defaultdict(lambda: {"name": "-", "roll": "-", "marks": -1})
        for r in results:
            if r["name"] == "Not Found": 
                continue
            for s in r["subjects"]:
                m = int(s["obtained"])
                if m > topper[s["code"]]["marks"]:
                    topper[s["code"]] = {"name": r["name"], "roll": r["roll"], "marks": m}

        return render_template("results.html", results=results, topper=topper)

    return render_template("index.html")


@app.route("/detail/<roll>")
def detail(roll):
    data = cache.get(int(roll))
    return render_template("detail.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)