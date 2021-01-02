from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from hse.models import Post, Meta, Person, Branch, Tag, Section, db_connect, create_table


class EmptyPostsPipeline:

    def process_item(self, item, spider):
        """Removes posts with no content"""
        if "text" not in item:
            raise DropItem('Empty post found.')
        return item


class SavePostsPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        post = Post()
        meta = Meta()

        post.title = item['title']
        post.description = item['description']
        post.text = item['text']

        meta.link = item['link']
        meta.campus = item['campus']
        meta.date = item['date']
        meta.visit_ts = item['visit_ts']

        if "tags" in item:
            for tag_name in item['tags']:
                tag = Tag(name=tag_name)
                if record := session.query(Tag).filter_by(name=tag_name).first():
                    tag = record
                meta.tags.append(tag)

        if "section" in item:
            for section_name in item['sections']:
                section = Section(name=section_name)
                if record := session.query(Section).filter_by(name=section_name).first():
                    section = record
                meta.sections.append(section)

        if "branches" in item:
            for branch_name in item['branches']:
                branch = Branch(name=branch_name)
                if record := session.query(Branch).filter_by(name=branch_name).first():
                    branch = record
                meta.branches.append(branch)

        if "people" in item:
            for full_name in item['people']:
                person = Person(name=full_name)
                if record := session.query(Person).filter_by(name=full_name).first():
                    person = record
                meta.people.append(person)

        post.meta = meta

        try:
            session.add(post)
            session.commit()

        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
            raise

        finally:
            session.close()

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        if session.query(Meta).filter_by(link=item['link']).first():
            raise DropItem("Duplicate item found.")
            session.close()
        else:
            return item
            session.close()
