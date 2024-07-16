from pathlib import Path

import pandas as pd

import pydfy.models as pf

LOREM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""


def main():
    iris_df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
    taxi_df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/taxis.csv")
    length_figure = iris_df.hist("sepal_length")[0][0].get_figure()
    ax = iris_df.hist("sepal_width")
    width_figure = ax[0][0].set_xlabel("Sepal Width").get_figure()

    pf.PDF(
        [
            pf.Title("My Report Title Spanning Multiple Columns", col_span=2),
            pf.Image(Path(__file__).parent / "logo.png"),
        ],
        pf.Section("Documentation"),
        [pf.Paragraph("<b>This</b> <i>is</i> a <b>test</b> " + LOREM), pf.Paragraph("<b>This</b> isn't " + LOREM)],
        pf.Section("KPIs Section"),
        [
            pf.Number(iris_df.shape[0], "Sample size"),
            pf.Number(len(iris_df.species.unique()), "Unique species"),
            pf.Number(iris_df.sepal_length.max(), "Max Sepal Length"),
        ],
        [
            pf.KPI(round(taxi_df["tip"].mean(), 2), 3, "Average Tip"),
            pf.KPI(taxi_df[taxi_df["tip"] < 1].shape[0], 1, "Tips under 1$"),
        ],
        pf.Table(iris_df.head(10), "Iris dataset"),
        [pf.Figure(width_figure), pf.Figure(length_figure)],
        pf.PageBreak(),
        pf.Section("Detail View"),
        pf.Table([[1, 2], [3, 4], [5, 100]], "My Table", ["a", "b"]),
        [pf.Table([[1, 2], [3, 4]], "Info A"), pf.Table([[1, 2], [3, 4]], "Info B")],
        pf.Table(taxi_df[["pickup", "distance", "fare", "tip", "tolls", "total", "payment"]].head(75), "Taxi dataset"),
    ).render(css="blue.css")


if __name__ == "__main__":
    main()
