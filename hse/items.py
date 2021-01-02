import re
import dateparser
from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join
from bs4 import BeautifulSoup


def normalize(html):
    soup = BeautifulSoup(html, features='lxml')

    # for i in ['.lead-in', '[class*="caption"]', '[class*="picture"]', '[class*="image"]']:
    for i in ['[class*="caption"]', '[class*="picture"]', '[class*="image"]']:
        if tag := soup.select(i):
            for el in tag:
                el.decompose()

    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


def process_tags(tags):
    return tags if ' '.join(tags).strip() else None


def convert_date(text):
    text = normalize(text)
    dt = dateparser.parse(text)
    return dt


class PostItem(Item):
    visit_ts = Field(
        output_processor=TakeFirst()
    )
    link = Field(
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
    date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    text = Field(
        input_processor=MapCompose(normalize),
        output_processor=Join()
    )
    sections = Field()
    tags = Field(
        input_processor=MapCompose(process_tags)
    )
    people = Field()
    branches = Field(
        input_processor=MapCompose(normalize)
    )

    def __str__(self):
        return ''
