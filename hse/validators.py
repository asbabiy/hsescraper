from schematics.models import Model
from schematics.types import URLType, StringType, ListType, DateTimeType, DateType


class PostItem(Model):
    visit_ts = DateTimeType(required=True)
    date = DateType(required=True)

    link = URLType(required=True)
    parent_link = URLType(required=True)
    campus = StringType(required=True)
    sections = StringType(required=True)

    title = StringType(required=True)
    description = StringType()
    text = StringType(required=True)

    tags = ListType(StringType)
    people = ListType(StringType)
    branches = ListType(StringType)
