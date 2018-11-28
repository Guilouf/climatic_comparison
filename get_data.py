"""
https://power.larc.nasa.gov/docs/v1/
"""

import requests
import csv
from database import DataLine, ses
from datetime import datetime


class GetData:
        API_URL = 'https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py'

        def __init__(self, location, latitude, longitude, start_date, end_date, param_list, elevation=None):
            self.location = location
            self.latitude = latitude,
            self.longitude = longitude
            self.start_date = start_date
            self.end_date = end_date
            self.param_list = param_list
            self.elevation = elevation

            self.shaped_data = self.shaping()

        def get_smth(self):

            para = {'request': 'execute',
                    'identifier': 'SinglePoint',
                    'lat': self.latitude,
                    'lon': self.longitude,
                    'siteElev': self.elevation,
                    'parameters': ','.join(self.param_list),
                    'startDate': self.start_date,
                    'endDate': self.end_date,
                    'tempAverage': 'DAILY',
                    'outputList': 'JSON',
                    'user': 'anonymous',
                    'userCommunity': 'AG'}

            return requests.get(self.API_URL, params=para)

        def shaping(self):
            response_json = self.get_smth().json()
            self.param_real_list = response_json['parameterInformation']
            # il y a parfois plus de parametres ds la réponse
            data_dict = response_json['features'][0]['properties']['parameter']
            # [print(len(dat)) for dat in data_dict.values()]
            # faudrait vérifier qu'il n'y ai pas de trous dans les dates

            flipped = {}
            for key, value in data_dict.items():
                for subkey, subval in value.items():
                    flipped.setdefault(subkey, {})[key] = subval

            return flipped

        def to_csv(self):
            with open('output.csv', 'w', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
                writer.writerow(['date', *self.param_real_list.keys()])  # order ok in 3.6
                for time, value in self.shaped_data.items():  # maintenant les dicos sont ordonnés
                    writer.writerow([time, *value.values()])

        def to_database(self):
            object_list = []
            for date, values in self.shaped_data.items():
                try:
                    obj = DataLine(date=datetime.strptime(date, '%Y%m%d'),
                                   sky_insolation=values['ALLSKY_SFC_SW_DWN'],
                                   precipitation=values['PRECTOT'],
                                   temperature=values['T2M'],
                                   temperature_max=values['T2M_MAX'],
                                   temperature_min=values['T2M_MIN'],
                                   location=self.location,
                                   )
                    object_list.append(obj)
                except ValueError:  # une valeur manquante dans la ligne
                    pass

            # a ne surtout pas mettre ds la boucle, ca fait des integrity error et tu sais pas d'ou ca viens..
            ses.bulk_save_objects(object_list)
            ses.commit()


if __name__ == '__main__':
    import json

    param_list = ['T2M', 'T2M_MIN', 'T2M_MAX', 'PS', 'PRECTOT', 'ALLSKY_SFC_SW_DWN']

    with open('locations.json', 'r') as locations_file:
        locations = json.load(locations_file)

        for loc in locations:
            GetData(loc['essai'], *loc['gps'], *loc['dates'],
                    param_list,
                    elevation=loc['elevation']).to_database()
