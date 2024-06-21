import io
from base64 import b64encode
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

BASE_DIR = Path(__file__).parent.parent


@dataclass
class Component:
    template_path: str = field(kw_only=True)
    col_span: int = field(kw_only=True, default=1)


@dataclass
class _PDF:
    components: Iterable[Union[Iterable[Component], Component]]

    def render(self, *args, **kwargs):
        from pydfy.renderer import render

        render(self, *args, **kwargs)


@dataclass
class PageBreak(Component):
    template_path: str = field(kw_only=True, default="src/partials/pagebreak.html")


@dataclass
class Title(Component):
    text: str

    template_path: str = field(kw_only=True, default="src/partials/title.html")


@dataclass
class Section(Component):
    text: str

    template_path: str = field(kw_only=True, default="src/partials/section.html")


@dataclass
class Number(Component):
    number: Union[int, float]
    title: str

    template_path: str = field(kw_only=True, default="src/partials/number.html")


@dataclass
class Paragraph(Component):
    content: str

    template_path: str = field(kw_only=True, default="src/partials/paragraph.html")


@dataclass
class Image(Component):
    path: Path

    @property
    def _mime_type(self) -> str:
        return "image/png"

    @property
    def _base64_data(self) -> str:
        return b64encode(self.path.read_bytes()).decode()

    template_path: str = field(kw_only=True, default="src/partials/image.html")


@dataclass
class Figure(Component):
    figure: Any  # type: ignore
    template_path: str = field(kw_only=True, default="src/partials/image.html")

    @property
    def _mime_type(self) -> str:
        return "image/png"

    @property
    def _base64_data(self) -> str:
        buffer = io.BytesIO()
        self.figure.savefig(buffer, format="png", dpi=300)

        return b64encode(buffer.getvalue()).decode()


@dataclass
class Table(Component):
    rows: Union[list[list[str]], Any]  # type: ignore # noqa
    title: str

    headers: list[str] = field(default_factory=list)
    template_path: str = field(kw_only=True, default="src/partials/table.html")

    @property
    def _rows(self) -> list:
        if self.rows.__class__.__module__ == "pandas.core.frame" and self.rows.__class__.__name__ == "DataFrame":
            return self.rows.values.tolist()  # type: ignore

        if self.rows.__class__.__module__ == "polars.dataframe.frame" and self.rows.__class__.__name__ == "DataFrame":
            return self.rows.rows()  # type: ignore

        return self.rows

    @property
    def _headers(self) -> list:
        if self.headers:
            return self.headers

        if self.rows.__class__.__name__ == "DataFrame":  # This works for both Polars and Pandas
            return list(self.rows.columns)  # type: ignore

        return []


def PDF(*rows) -> _PDF:
    return _PDF(rows)
