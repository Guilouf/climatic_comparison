import matplotlib.pyplot as plt
from database import DataLine, ses, year, month, day, between
import matplotlib


def get_col(col_name, queryset):
    return [getattr(obj, col_name) for obj in queryset]


matplotlib.use('Qt5Agg')  # to force pycharm to not use its SciView

query_vendee = ses.query(DataLine).filter_by(location='vendee').\
    filter(DataLine.date.between('2018-02-01', '2018-02-15'))

# query_charente = ses.query(DataLine).filter_by(location='charente_maritime').filter(month > 2, month < 5)
query_charente = ses.query(DataLine).filter_by(location='charente_maritime', date_month_day=(3, 25))

print(get_col('temperature', query_charente))

fig, ax = plt.subplots()
fig.autofmt_xdate()


ax.plot(get_col('date', query_charente),
        get_col('temperature', query_charente), label='temp_charente_2018')

ax.legend()
plt.show()
