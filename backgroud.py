import threading
from models import Seing
from sqlalchemy import create_engine
from sqlalchemy.orm import query, sessionmaker

engine = create_engine('sqlite:///seing.db')
Session = sessionmaker(bind=engine)
session = Session()

class Background():

    def __init__(self, db_records):
        self.db_records = db_records


    def run_background_commiter(self) -> None:
        thread = threading.Thread(target=self.add_and_commit())
        thread.start()


    def add_and_commit(self) -> None:
        not_to_have = ["New account", "Forgotten password", "Error", "Notice", "EAPI", "403 Forbidden"]
        for item in self.db_records:
            site_instance = session.query(Seing).filter_by(site=item['site']).first()
            url_instance = session.query(Seing).filter_by(url=item['url']).first()
            if site_instance or url_instance or item['site'] in not_to_have:
                continue
            domain = Seing(**item)
            session.add(domain)
        session.commit()
