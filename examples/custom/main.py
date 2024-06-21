from dataclasses import dataclass, field

import pydfy.models as pf


@dataclass
class TwoNumbers(pf.Component):
    number_1: int
    number_2: int
    title: str

    template_path: str = field(default="two_numbers.html", kw_only=True)


def main():
    pf.PDF(pf.Title("Report"), [TwoNumbers(3141, 5926, "Pi"), TwoNumbers(5358, 9793, "Thon")]).render()


if __name__ == "__main__":
    main()
