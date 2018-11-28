# https://power.larc.nasa.gov/docs/v1/

import requests
import csv


class GetData:
        API_URL = 'https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py'

        def __init__(self, latitude, longitude, start_date, end_date, param_list, elevation=None):
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
            # print(self.shaped_data)
            with open('output.csv', 'w', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
                writer.writerow(['date', *self.param_real_list.keys()])  # order ok in 3.6
                for time, value in self.shaped_data.items():  # maintenant les dicos sont ordonnés
                    writer.writerow([time, *value.values()])
                    print([time, *value.values()])


msg = GetData(44.2490, 1.5659, 20160301, 20160331, ['T2M', 'PS', 'ALLSKY_SFC_SW_DWN'], elevation=274.62).to_csv()


# print('hoho', msg, msg.text, msg.url)
# data = msg.json()['features'][0]['properties']['parameter']
# print(data)

# faut iterer par date tous les params, et virer les lignes incompletes..