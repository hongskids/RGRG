from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy import create_engine

now = datetime.now() #get current datetime(format: YYYY-MM-DD TIME)
DB = create_engine('mysql+mysqldb://root:hongskids1!@127.0.0.1/site?charset=utf8', echo=True)
Base = declarative_base()

#Table 'crawl_item'
class crawl_item(Base):
    __tablename__ = 'crawl_item'

    crawl_id = Column(Integer, primary_key=True)
    site_id = Column(Integer)
    url = Column(String(500))
    title = Column(String(100))
    attribute = Column(Text(4294000000)) #LongText Type
    views = Column(Integer)
    reg_date = Column(Date)
    deadline = Column(Date)
    crawl_date = Column(Date)
    state = Column(Integer)

    def __init__(self, site_id, url, title, state, views=0, reg_date = None, deadline=None, attribute=None):
        self.site_id = site_id
        self.url = url
        self.title = title
        self.attribute = attribute
        self.views = views
        self.deadline = deadline
        self.crawl_date = now
        self.state = state
        self.reg_date = reg_date  #insert current date


#Table 'site'
class site(Base):
    __tablename__ = 'site'

    site_id = Column(Integer, primary_key=True)
    name = Column(String(20))
    url = Column(String(100))

    def __init__(self, name, url):
        self.name = name
        self.url = url

#Table 'content'
class content(Base):
    __tablename__ = 'content'

    content_id = Column(Integer, primary_key=True)
    crawl_item_id = Column(Integer)
    image = Column(String(100))
    post_content = Column(Text(4294000000))

    def __init__(self, crawl_item_id, post_content, image = None):
        self.crawl_item_id = crawl_item_id
        self.post_content = post_content
        self.image = image