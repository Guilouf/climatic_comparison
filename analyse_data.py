import matplotlib.pyplot as plt
from database import DataLine, ses

query_vendee = ses.query(DataLine).filter_by(location='vendee').filter(DataLine.date.between('2015-03-01', '2017-03-15'))
query_charente = ses.query(DataLine).filter_by(location='charente').filter(DataLine.date.between('2015-03-01', '2017-03-15'))


fig, ax = plt.subplots()


time = [q.date for q in query_vendee]
temp = [q.temperature for q in query_vendee]
sky = [q.sky_insolation for q in query_vendee]

ax.plot(time, temp, label='temp_vendée')
ax.plot(time, sky, label='sky_vendée')

time_charent = [q.date for q in query_charente]
temp_charente = [q.temperature for q in query_charente]
sky_charente = [q.sky_insolation for q in query_charente]

ax.plot(time_charent, temp_charente, label='temp_charente')

ax.legend()

plt.show()
