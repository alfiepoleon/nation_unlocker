import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def parseNationUrl(url: str) -> BeautifulSoup:
    page = requests.get(url)

    if(page.status_code != 200):
        raise Exception("Invalid url")
    soup = BeautifulSoup(page.content, 'html.parser')
    blocking_tag = soup.find("section", class_="teasers-row")
    blocking_tag.decompose()

    for data in soup(['script']):
        # Remove Javascript
        data.decompose()

    for data in soup.find_all("div", class_="content-page-ad_wrap"):
        # Remove ads
        data.decompose()

    for data in soup.find_all("div", class_="paragraph-wrapper"):
        # Remove other classes & styles in paragraphs with contest
        data['class'] = "paragraph-wrapper"
        data['style'] = ""

    for data in soup(['link']):
        # Replace links
        if not(data["href"].startswith("http")):
            data["href"] = "https://nation.africa" + data["href"]

    for data in soup.findAll("img"):
        # Replace img-links links
        # Replace data-src links
        try:
            if not(data["data-src"].startswith("http")):
                data["data-src"] = "https://nation.africa" + data["data-src"]
        except KeyError:
            try:
                if not(data["src"].startswith("http")):
                    data["src"] = "https://nation.africa" + data["src"]
            except KeyError:
                pass

        # Replace data-srcset links
        try:
            data_srcset = [x.strip() for x in data["data-srcset"].split(",")]

            data_srcset = ["https://nation.africa" +
                           d if not(d.startswith("http")) else d for d in data_srcset]
            data["data-srcset"] = ",\n".join(data_srcset)
        except KeyError:
            pass

        # Replace srcset links
        try:
            srcset = [x.strip() for x in data["srcset"].split(",")]

            srcset = ["https://nation.africa" +
                      d if not(d.startswith("http")) else d for d in srcset]
            data["srcset"] = ",\n".join(srcset)
        except KeyError:
            pass

    soup_str = str(soup)
    # with open("res/article.html", "w", encoding='utf-8') as file:
    #     file.write(soup_str)

    return soup_str


@app.route("/", methods=('GET', 'POST'))
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        link = request.form['link']
        error = None

        if not link:
            error = 'Nation link is required.'

        if error is not None:
            flash(error)
            return render_template('index.html')

        # print(f'link: ${link}')
        # parseNationUrl(link)
        # return parseNationUrl(link)
        return redirect(url_for("fetch", link=link))


@app.route("/fetch", methods=(['GET']))
def fetch():
    link = request.args.get('link', '')

    return parseNationUrl(link)


if __name__ == "__main__":
    app.run()
