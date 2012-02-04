import datetime
import string

def DieselDateToDatetime(d):	
	if d[0]==u'С':
		dt=datetime.date(1,1,1)
		dt=dt.today()
		dd=dt.day
		mm=dt.month
		yy=dt.year
	elif d[0]==u'В':
		dt=datetime.date(1,1,1)
		dt=dt.today()
		dt=dt-datetime.timedelta(days=1)
		dd=dt.day
		mm=dt.month
		yy=dt.year
	else:
		cm=d.index(',')
		dt=d[0:cm]
		qq=string.split(dt,'.')
		dd=int(qq[0])
		mm=int(qq[1])
		yy=int(qq[2])
		
	cm=d.index(',')
	d+=" "
	dt=d[cm+1:-1]
	qq=string.split(dt,':')
	ho=int(qq[0])
	mi=int(qq[1])

	return datetime.datetime(yy,mm,dd,ho,mi)

