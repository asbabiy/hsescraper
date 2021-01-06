import re
import dateparser
from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join
from bs4 import BeautifulSoup


def normalize(html):
    soup = BeautifulSoup(html, features='lxml')

    for i in ['[class*="caption"]', '[class*="picture"]', '[class*="image"]']:
        if tag := soup.select(i):
            for el in tag:
                el.decompose()

    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text if text else ('N/A',)


def process_na(item):
    return item.strip() if ' '.join(item).strip() else ('N/A',)


def convert_date(html):
    soup = BeautifulSoup(html, features='lxml')
    date = ' '.join(i.get_text() for i in soup.find_all('div')[1:])
    dt = dateparser.parse(date)
    return dt


class PostItem(Item):
    visit_ts = Field(
        output_processor=TakeFirst()
    )
    date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    link = Field(
        output_processor=TakeFirst()
    )
    parent_link = Field(
        output_processor=TakeFirst()
    )
    campus = Field(
        output_processor=TakeFirst()
    )
    title = Field(
        input_processor=MapCompose(normalize),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(normalize),
        output_processor=TakeFirst()
    )
    text = Field(
        input_processor=MapCompose(normalize),
        output_processor=Join()
    )
    section = Field(
        output_processor=TakeFirst()
    )
    tags = Field(
        input_processor=MapCompose(process_na)
    )
    people = Field(
        input_processor=MapCompose(process_na)
    )
    branches = Field(
        input_processor=MapCompose(normalize)
    )

    def __str__(self):
        return f'Post: {self["link"]}.'
