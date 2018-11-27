import matplotlib.pyplot as plt
from database import DataLine, ses

query_vendee = ses.query(DataLine).filter_by(location='vendee').filter(DataLine.date.between('2015-03-01', '2017-03-15'))
query_charente = ses.query(DataLine).filter_by(location='charente').filter(DataLine.date.between('2015-03-01', '2017-03-15'))


fig, ax = plt.subplots()


time = [q.date for q in query_vendee]
temp = [q.temperature for q in query_vendee]
sky = [q.sky_insolation for q in query_vendee]



ax.plot(time, temp)
ax.plot(time, sky)



time_charent = [q.date for q in query_charente]
temp_charente = [q.temperature for q in query_charente]
sky_charente = [q.sky_insolation for q in query_charente]

ax.plot(time, temp_charente)

plt.show()
