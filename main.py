import sys
import jinja2
from flask import Flask

app = Flask(__name__)


def generate_html():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    template = env.get_template('template.html')
    return template.render()


@app.route("/")
def render_html():
    return generate_html()


def serve():
    app.run()


def generate():
    print(generate_html())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
    else:
        generate()
