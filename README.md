# Pydfy: PDF Generation Made Simple

<div align="center">

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/BiteStreams/pydfy/blob/main/.pre-commit-config.yaml)
[![Tests](https://github.com/BiteStreams/pydfy/actions/workflows/tests.yml/badge.svg)](https://github.com/BiteStreams/pydfy/actions/workflows/tests.yml)
[![License](https://img.shields.io/github/license/BiteStreams/pydfy)](https://github.com/BiteStreams/pydfy/blob/main/LICENSE)

</div>

Pydfy makes creating beautiful PDF reports as simple as you'd hope it to be.
In practice, this is often not the case as:
- Not the whole team knows LaTeX
- The support for this in BI tooling is lacking
- Webpages are usually not tuned for PDF exports
- PDF builders are too complex to get something out the door by the end of the week

## Installation

First, make sure `tailwindcss` is in your `PATH`, which for Linux means:
```shell
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss
```
Check https://github.com/tailwindlabs/tailwindcss/releases/latest to find the matching binary for your system.

Also make sure to install Chromium:
```shell
apt-get update && apt-get install -y chromium  # Example using apt-get
brew install --cask chromium                   # Homebrew example for macOS
```

Now run:
```shell
pip install pydfy
```
And you should be good to go. Optionally install the extra dependencies as well:
```shell
pip install "pydfy[pandas,matplotlib]"
```

## Usage

### Example
```python3
import pydfy.models as pf
import pandas as pd

sales_df = pd.read_csv("sales.csv")
orders_last_week = sales_df[sales_df["week"] == 10]
avg_price = sales_df["price"].mean()

pdf = pf.PDF(
    pf.Title(text="Sales Report"),
    [pf.Number(orders_last_week, title="Orders last week"), pf.Number(avg_price, title="Average price")],
    [pf.Table(sales_df, "Sales table"), sales_df.plot("hist")],
)
pdf.render()
```

The main entrypoint is defined, in this context, by the `pf.PDF` function,
which accepts the rows of the PDF as arguments and wraps a `pf._PDF` model for ease of use.
A row here can either be a single component or an iterable of components, as shown in the example above.

### Overview of Components
```python3
Component(template_path=..., col_span=...)  # Abstract component, args apply to all other components

Table(rows=..., title=..., headers=...)
Number(number=..., tiele=...)

Image(path=...)
Figure(figure=...)

Title(text=...)
Section(text=...)
Paragraph(content=...)
PageBreak(...)
```

### Output location
By default, this renders a PDF file called `out.pdf` in the current working directory.
To control the location of the build files, you can do:
```python3
# Change the name of the rendered report and store the intermediate html and css files in the /build directory
pdf.render(out="report.pdf", build_dir="/build")

# Save everything in the /data directory
pdf.render(out="/data/report.pdf", build_dir="/data")

# Equivalent to the previous line
os.environ["PYDFY_BUILD_DIR"] = "/data"
pdf.render(out="/data/report.pdf")
```

### Custom Components
You can create custom components with custom html templates as follows:
```python3
from dataclasses import dataclass, field

import pydfy.models as pf


@dataclass
class TwoNumbers(pf.Component):
    number_1: int
    number_2: int
    title: str

    template_path: str = field(default="two_numbers.html", kw_only=True)
```

Where the contents of `two_numbers.html` is:
```html
<div class="pf-two-numbers border-solid border border-gray-100">
    <div class="pf-two-numbers-title bg-gray-200 text-lg font-bold text-center align-top">{{ component.title }}</div>
    <div class="pf-two-numbers-content mt-2 text-center">
        <div class="grid grid-cols-2">
            <div class="text-3xl mb-2">{{ "{:,}".format(component.number_1) }}</div>
            <div class="text-3xl mb-2">{{ "{:,}".format(component.number_2) }}</div>
        </div>
    </div>
</div>
```

To see a working example, check out `examples/custom`.


### Custom CSS
You can add custom CSS to the compilation step:
```python3
pdf.render(css="blue.css")
```

Content of `my.css`, where the path should point to your pydfy install:
```css
@import "../../pydfy/template/src/base.css";

.pf-number-content {
    color: blue;
}
```

To see a working example, check out `examples/iris`.


### Using Docker

You could use Docker in the development process as follows:
```shell
docker build -t pydfy .
cd examples/iris
docker run -v $PWD/:/data pydfy /data/main.py  # The docker image is configured with PYDFY_BUILD_DIR=/data
```

## Contributing

```shell
poetry install --with dev --all-extras
```
