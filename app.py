import os
from typing import Callable, Dict, List, Optional, Self, Set
from urllib import parse, request

import pydantic
from bs4 import BeautifulSoup, ResultSet
from pydantic import BaseModel, Field

FilterCallableT = Callable[[ResultSet], bool]


class HtmlFilter(BaseModel):
    by: str
    attr_filters: Optional[Dict[str, str]] = None
    call_filter: Optional[FilterCallableT] = None


class Customer(BaseModel):
    company: str
    logo_url: str


class Page(BaseModel):
    url: str
    customers: Optional[List[Customer]] = Field(default_factory=list)

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        return BeautifulSoup(request.urlopen(url).read(), "html.parser")

    @staticmethod
    def parse_html(url: str, html_filter: HtmlFilter) -> Set:
        soup = Page.get_soup(url=url)
        found = (
            soup.find_all(html_filter.by, html_filter.attr_filters)
            if html_filter.attr_filters
            else soup.find_all(html_filter.by)
        )

        if not html_filter.call_filter:
            return set(found)

        return {f for f in found if html_filter.call_filter(f)}

    @classmethod
    def from_url(cls, url: str, html_filter: HtmlFilter) -> Self:
        raw_customers = cls.parse_html(url=url, html_filter=html_filter)

        obj: Dict[str, str | List[Customer]] = {"url": url}
        if not raw_customers:
            return pydantic.parse_obj_as(cls, obj)

        obj["customers"] = [
            Customer(company=raw_customer.get("alt"), logo_url=parse.urljoin(url, raw_customer.get("src")))
            for raw_customer in raw_customers
        ]

        return pydantic.parse_obj_as(cls, obj)

    def report_customers(self) -> str:
        markdown_string = f"# {self.url}\n\n"

        if not self.customers:
            markdown_string += "No customers\n\n"
            return markdown_string

        markdown_string += "## Customers\n\n"

        for customer in self.customers:
            customer_name = customer.company if customer.company != "" else "unknown"
            markdown_string += f"- [{customer_name}]({customer.logo_url})\n"

        return markdown_string


class Pages(BaseModel):
    pages: Dict[str, Page]

    @classmethod
    def from_urls(cls, url_filters: Dict[str, HtmlFilter]) -> Self:
        return pydantic.parse_obj_as(
            cls,
            {
                "pages": {
                    url: Page.from_url(url=url, html_filter=html_filter) for url, html_filter in url_filters.items()
                }
            },
        )

    def report_customers(self) -> str:
        return "\n\n".join([page.report_customers() for page in self.pages.values()])

    def save_report(self, output_path: str) -> None:
        os.makedirs(output_path, exist_ok=True)

        with open(os.path.join(output_path, "customers.md"), "w") as file:
            file.write(self.report_customers())

        return None


if __name__ == "__main__":

    def deel_call_filter(found: ResultSet) -> bool:
        previous_class = found.find_previous().get("class")
        return previous_class and previous_class[0] == "single-image"

    scale_filter = HtmlFilter(by="img", attr_filters={"class": "logo-grid_dark__2JTFY"})
    webflow_filter = HtmlFilter(by="img", attr_filters={"class": "intro-logos_logo"})
    deel_filter = HtmlFilter(by="img", attr_filters={"loading": "lazy"}, call_filter=deel_call_filter)

    url_filters = {
        "https://scale.com/": scale_filter,
        "https://www.deel.com/": deel_filter,
        "https://webflow.com/": webflow_filter,
    }

    pages = Pages.from_urls(url_filters=url_filters)
    pages.save_report("./temp/")


def test_customer_search():
    def deel_call_filter(found: ResultSet) -> bool:
        previous_class = found.find_previous().get("class")
        return previous_class and previous_class[0] == "single-image"

    deel_filter = HtmlFilter(by="img", attr_filters={"loading": "lazy"}, call_filter=deel_call_filter)

    url_filters = {
        "https://www.deel.com/": deel_filter,
    }

    obj = Pages.from_urls(url_filters=url_filters)

    assert len(obj.pages) == 1

    deel_page = obj.pages.pop("https://www.deel.com/", None)

    assert isinstance(deel_page, Page)
    assert len(deel_page.customers) == 13
