from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship

eng = create_engine('sqlite:///database.db')
# supprime la base en case de changement de schéma..
Base = declarative_base()


class DataLine(Base):
    __tablename__ = 'DataLine'
    __table_args__ = (
        UniqueConstraint('date', 'location', 'sky_insolation', 'conversion', 'temperature', name='prixunique'),
        # pas besoin de les avoir toutes ca evite déjà les doublons
    )
    __mapper_args__ = {
        "order_by": 'date'
    }

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    location = Column(String)

    sky_insolation = Column(Float)
    conversion = Column(Float)
    precipitation = Column(Float)
    temperature = Column(Float)
    temperature_max = Column(Float)
    temperature_min = Column(Float)

    @property
    def diff(self):
        return self.temperature_max - self.temperature_min


Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()

# try:
#     obj = DataLine(date=datetime.strptime(line[0], '%d/%m/%Y'),
#                    sky_insolation=to_float(line[1]),
#                    conversion=to_float(line[2]),
#                    precipitation=to_float(line[3]),
#                    temperature=to_float(line[4]),
#                    temperature_max=to_float(line[5]),
#                    temperature_min=to_float(line[6]),
#                    location=line[7],
#                    )
#     object_list.append(obj)
# except ValueError:  # une valeur manquante dans la ligne
#     pass
#
# ses.bulk_save_objects(object_list)
# ses.commit()




