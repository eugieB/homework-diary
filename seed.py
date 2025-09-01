from sqlalchemy import create_engine
from models import Base, School, Learner, Homework
from datetime import datetime, timedelta

engine = create_engine("sqlite:///./homework.db", echo=False)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
db = Session()

s = School(name="Demo SA School"); db.add(s); db.commit()
l = Learner(name="Sipho", school_id=s.id); db.add(l); db.commit()
db.add(Homework(task="Math p.12", special_focus="fractions", learner_id=l.id,
                date=datetime.utcnow()-timedelta(days=2)))
db.commit()
print("DB seeded")
