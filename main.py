import sys
import requests
import argparse
import jinja2
from flask import Flask
import logging
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_meta(soup, tag, name):
    tag = soup.find("meta", {tag: name})
    if tag:
        return tag['content']
    else:
        return None


def get_title(soup):
    title = get_meta(soup, "property", "og:title")
    if not title:
        title = get_meta(soup, "name", "title")
    if not title:
        title = soup.title.string
    return title


def get_author(soup):
    author = get_meta(soup, "property", "author")
    if not author:
        author = get_meta(soup, "property", "article:author")
    if not author:
        author = get_meta(soup, "property", "og:author")
    if not author:
        author = get_meta(soup, "property", "og:site_name")
    if not author:
        author = get_meta(soup, "name", "site_name")
    if not author:
        author = ""
    return author


def get_description(soup):
    description = get_meta(soup, "name", "description")
    if not description:
        description = get_meta(soup, "property", "og:description")
    return description


def fetch(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    description = get_description(soup)
    author = get_author(soup)
    title = get_title(soup)
    return {
        "link": link,
        "title": title,
        "author": author,
        "description": description
    }


def generate_html(args):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    template = env.get_template('template.html')
    issue = 1
    with open(args.articles) as f:
            article_links = f.readlines()
            article_links = [x.strip() for x in article_links]
    articles = [fetch(link) for link in article_links]
    with open(args.shorts) as f:
            short_links = f.readlines()
            short_links = [x.strip() for x in short_links]
    shorts = [fetch(link) for link in short_links]
    return template.render(
        subject="Spark Weekly Issue {}".format(issue),
        articles=articles,
        shorts=shorts)


@app.route("/")
def render_html():
    return generate_html(args)


def serve(args):
    app.run(debug=True)


def generate(args):
    print(generate_html(args))


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", help="print|serve", choices=["print", "serve"])
    parser.add_argument("-a", "--articles", help="File containing the article links", required=True)
    parser.add_argument("-s", "--shorts", help="File containing the short article links", required=True)
    return parser


if __name__ == "__main__":
    args = parser().parse_args()
    if args.command == "serve":
        serve(args)
    else:
        generate(args)
