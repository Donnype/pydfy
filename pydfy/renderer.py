import base64
import os
import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.common import NoSuchDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.print_page_options import PrintOptions

from pydfy.models import _PDF, BASE_DIR


def render(
    pdf: _PDF,
    out: Path | str | None = None,
    *,
    build_dir: Path | str = BASE_DIR / "build",
    css: Path | str | None = None,
) -> None:
    build_dir = Path(build_dir)

    if not build_dir.exists():
        build_dir.mkdir(exist_ok=True, parents=True)

    if not out:
        out = Path(os.getenv("PYDFY_BUILD_DIR", ".")) / Path("out.pdf")

    out = Path(out)

    _render_template(BASE_DIR / "pydfy/template/src/template.html", build_dir / "out.html", pdf)
    _compile_css(build_dir, css)
    _print_to_pdf(build_dir / "out.html", out)


def relative_to(path: Path, other: Path):
    """A Python 3.12 feature almost copied one on one to have the "walk_up" functionality"""

    for step, parent in enumerate([Path(other)] + list(Path(other).parents)):
        if path.is_relative_to(parent):
            break
        elif parent.name == "..":
            raise ValueError(f"'..' segment in {str(other)!r} cannot be walked")
    else:
        raise ValueError(f"{str(path)!r} and {str(other)!r} have different anchors")

    parts = [".."] * step + str(path).split("/")[1:][len(str(parent).split("/")[1:]) :]
    return Path(*parts)


def _render_template(template_file: Path, out: Path, pdf_arguments: _PDF) -> None:
    template_dir = template_file.parent.parent
    env = Environment(loader=FileSystemLoader([template_dir, Path().absolute()]))  # Add CWD for custom components

    template = env.get_template(str(relative_to(template_file, template_dir)))
    rendered_html = template.render({"pdf": pdf_arguments})

    out.write_text(rendered_html)


def _compile_css(build_dir: Path, css: Path | str | None) -> None:
    base = str(BASE_DIR / "pydfy" / "template" / "src" / "base.css")
    out = str(build_dir / "out.css")

    args = [
        "tailwindcss",
        "-i",
        base if not css else str(Path(css)),
        "-o",
        out,
        "--content",
        str(relative_to(build_dir, Path().absolute())) + "/*.html",
    ]
    # if css:

    subprocess.run(args, capture_output=True)


def _print_to_pdf(rendered_template_file: Path, output_path: Path) -> None:
    # Pass the relevant CLI parameters
    options = Options()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless=new")  # for Chrome >= 109
    options.add_argument("--headless")

    try:
        driver = webdriver.Chrome(options=options)
    except NoSuchDriverException:
        driver = webdriver.Chrome(options=options, service=Service(executable_path="/usr/bin/chromedriver"))

    driver.get(f"file://{str(rendered_template_file.resolve())}")

    # Set size to A4
    print_options = PrintOptions()
    print_options.page_width = 21.0
    print_options.page_height = 29.7
    print_options.scale = 1

    pdf_content = base64.b64decode(driver.print_page(print_options))
    output_path.write_bytes(pdf_content)
