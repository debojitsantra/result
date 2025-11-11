import subprocess
from bs4 import BeautifulSoup

URL = "https://result.wb.gov.in/result.php"

def fetch_html(roll, reg):
    roll = str(roll)
    reg = str(reg)

    rollpre = roll[:6]
    rollno = roll[6:]

    cmd = [
        "curl",
        "--silent",
        "--insecure",
        "--tlsv1",
        "--ciphers", "DEFAULT:@SECLEVEL=1",   # ✅ legacy support
        "-X", "POST",
        "-d", f"rollpre={rollpre}&rollno={rollno}&regnno={reg}",
        URL
    ]

    try:
        return subprocess.check_output(cmd, text=True)
    except:
        return None


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    if len(tables) < 3:
        return None

    info = tables[0].find_all("tr")
    name = info[0].find_all("td")[1].text.strip()
    roll = info[1].find_all("td")[1].text.strip()
    reg  = info[2].find_all("td")[1].text.strip()

    subjects = []
    for row in tables[1].find_all("tr")[1:]:
        td = row.find_all("td")
        subjects.append({
            "type": td[0].text.strip(),
            "code": td[1].text.strip(),
            "full": td[2].text.strip(),
            "pass": td[3].text.strip(),
            "obtained": td[4].text.strip(),
            "percent": td[5].text.strip(),
            "percentile": td[6].text.strip(),
            "result": td[7].text.strip()
        })

    totals = tables[2].find_all("tr")
    total_marks = totals[0].find_all("td")[1].text.strip()
    percentage  = totals[1].find_all("td")[1].text.strip()
    supplementary = totals[2].find_all("td")[1].text.strip()

    return {
        "name": name,
        "roll": roll,
        "reg": reg,
        "subjects": subjects,
        "total_marks": total_marks,
        "percentage": percentage,
        "supplementary": supplementary
    }