from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, extract
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import sessionmaker, validates

eng = create_engine('sqlite:///database.db')
# supprime la base en case de changement de schéma..
Base = declarative_base()


class DataLine(Base):
    __tablename__ = 'DataLine'
    __table_args__ = (
        UniqueConstraint('date', 'location', 'sky_insolation', 'temperature', name='prixunique'),
        # pas besoin de les avoir toutes ca evite déjà les doublons
    )
    __mapper_args__ = {
        "order_by": 'date'
    }

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    location = Column(String)

    sky_insolation = Column(Float)
    precipitation = Column(Float)
    temperature = Column(Float)
    temperature_max = Column(Float)
    temperature_min = Column(Float)

    @property
    def sky_insolation_convertion(self):
        """Converts the sky insolation incident from MJ/m²/jr to µmol/m²/s"""
        # je sais pas quel est le calcul mais ca fait pas très scientifique..
        return ((self.sky_insolation/86400)*1000000)*4.75*0.63

    @validates('sky_insolation', 'precipitation')
    def missing_data(self, key, field):
        """Check if there is no aberrant/missing values in these fields, return as N/A"""
        if field == -99:
            return None
        return field


Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()


year = extract('year', DataLine.date)
month = extract('month', DataLine.date)
day = extract('day', DataLine.date)
between = DataLine.date.between
