from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
import pytest

import pydfy.models as pf


@pytest.fixture
def out(tmp_path):
    return tmp_path / "out.pdf"


def test_render_list_table(tmp_path, out):
    pf.PDF(pf.Table([[0, 1], [2], [3, 4]], "T1"), [pf.Table([[0, 1]], "2"), pf.Table([[2], [3, 4]], "")]).render(
        out, build_dir=tmp_path
    )

    assert (tmp_path / "out.html").exists()
    assert (tmp_path / "out.css").exists()
    assert out.exists()
    assert len(out.read_bytes()) > 500


def test_render_pandas_table(tmp_path, out):
    df = pd.DataFrame([[123, 3, 3, 3], ["wow", "some", "df", None]], columns=["one", "two", 0, 1])
    pf.PDF([pf.Table([[0, 1], [2], [3, 4]], "Test")], pf.Table(df, "Df table")).render(out, build_dir=tmp_path)

    assert (tmp_path / "out.html").exists()
    assert (tmp_path / "out.css").exists()
    assert "wow</td>" in (tmp_path / "out.html").read_text()
    assert "::before" in (tmp_path / "out.css").read_text()
    assert len(out.read_bytes()) > 500


def test_render_polars_table(tmp_path, out):
    pl_df = pl.DataFrame([[123, 3, 3, 3], ["wow", "some", "df", None]])
    pf.PDF([pf.Table([[0, 1], [2], [3, 4]], "Test")], pf.Table(pl_df, "Polars table")).render(out, build_dir=tmp_path)
    assert (tmp_path / "out.html").exists()
    assert (tmp_path / "out.css").exists()
    assert len(out.read_bytes()) > 500


def test_render_numpy_table(tmp_path, out):
    np_df = np.array([[1, 2, 0], [3, 4, 5]])
    pf.PDF([pf.Table([[0, 1], [2], [3, 4]], "Test")], pf.Table(np_df, "Numpy table")).render(out, build_dir=tmp_path)

    assert (tmp_path / "out.html").exists()
    assert (tmp_path / "out.css").exists()
    assert len(out.read_bytes()) > 500


def test_render_custom_css(tmp_path, out):
    pf.PDF(pf.Number(3, "3")).render(out, build_dir=tmp_path, css=Path(__file__).parent / "stubs" / "test.css")

    assert "::before" in (tmp_path / "out.css").read_text()
    assert ".pf-number-content" in (tmp_path / "out.css").read_text()


def test_all_components(tmp_path, out):
    asset_dir = Path(__file__).parent / "stubs"
    df = pd.DataFrame([[123, 3, 3, 3], ["wow", "some", "df", None]], columns=["one", "two", 0, 1])
    figure = df.hist(1)[0][0].get_figure()

    pf.PDF(
        [
            pf.Title("My Beautiful Report with a very long title that I'd really like to keep", col_span=2),
            pf.Image(asset_dir / "hist.png"),
        ],
        pf.Section("Documentation"),
        [
            pf.Paragraph("<b>This</b> <i>is</i> a <b>test</b> "),
            pf.Paragraph("<b>This</b> <i>is</i> a <b>test</b> "),
        ],
        pf.Section("KPIs Section"),
        [
            pf.Number(df.shape[0], "Sample size"),
            pf.Number(df[1].max(), "Max"),
            pf.KPI(482.537, 595.092, "Compare"),
        ],
        pf.Table(df.head(10), "Test dataset"),
        [pf.Image(asset_dir / "hist.png"), pf.Figure(figure)],
        pf.PageBreak(),
        pf.Table([[1, 2], [3, 4], [5, 100]], "My Table", ["a", "b"]),
        [pf.Table([[1, 2], [3, 4]], "My Table"), pf.Table([[1, 2], [3, 4]], "My Table")],
    ).render(out, build_dir=tmp_path)

    assert (tmp_path / "out.html").exists()
    assert (tmp_path / "out.css").exists()
    assert len(out.read_bytes()) > 90000
