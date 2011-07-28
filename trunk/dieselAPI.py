import urllib
import urllib2
import cookielib
import re
import datetime


class Diesel:
#private fields
	__cookies=cookielib.CookieJar()
	__opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(__cookies))

#
# private methods
#
	def __init__(self):
		self.__opener.open('http://diesel.elcat.kg')
	def __getUserBirthDateById(self,userId):
		monthes={}
		monthes[u'Янв']=1
		monthes[u'Фев']=2
		monthes[u'Март']=3
		monthes[u'Апр']=4
		monthes[u'Май']=5
		monthes[u'Июнь']=6
		monthes[u'Июль']=7
		monthes[u'Авг']=8
		monthes[u'Сен']=9
		monthes[u'Окт']=10
		monthes[u'Ноя']=11
		monthes[u'Дек']=12
		response=self.__opener.open('http://diesel.elcat.kg/index.php?showuser='+str(userId))
		data=response.read().decode('cp1251')

		if response.geturl()=='http://diesel.elcat.kg/index.php':
			return None
		elif data.count(u'Возраст не указан')>0:
			return None
		else:
			result=re.search(u'<span id=\'pp-entry-born-text\'>(.+?)</span>',data)
			datestr=result.groups(1)
			result=re.search('(.+)-(.+)-(.+)',datestr[0])

			year=int(result.group(3))
			month=monthes[result.group(1)]
			day=int(result.group(2))
			date=datetime.date(year,month,day)
			return date



	def __setRatingById(self,userId,rating):
		url='http://diesel.elcat.kg/index.php?showuser='+str(userId)
		response=self.__opener.open(url)
		data=response.read().decode('cp1251')

		pattern='var ipb_md5_check         = "(.+?)";'
		result=re.search(pattern,data)
		md5_check=result.group(1)
		
		url='http://diesel.elcat.kg/index.php?s=&act=xmlout&do=member-rate&member_id=%s&rating=%s&md5check=%s'%(str(userId),str(rating),str(md5_check))
		response=self.__opener.open(url)
		return response.read()

#
# public methods
#
	def IsLogin(self):
		response=self.__opener.open('http://diesel.elcat.kg')
		data=response.read().decode('cp1251')
		if data.count('http://diesel.elcat.kg/index.php?act=Login&amp;CODE=03')>0:
			return True
		else:
			return False

	def GetUserBirthDate(self,user):
		if isinstance(user,int):
			return self.__getUserBirthDateById(user)
		elif isinstance(user,basestring):
			return self.__getUserBirthDateById(self.__getUserBirthDateByName(user))
		else:
			return None

	def GetIdByName(self,userName):
		userNameCoded=userName.decode('utf-8').encode('cp1251')
		name_data=urllib.urlencode({'name':userNameCoded})
		response=self.__opener.open('http://diesel.elcat.kg/index.php?act=members&name_box=begins',name_data)
		data=response.read().decode('cp1251')

		pattern='<!-- Entry for '+userName.decode('utf-8')
		pattern+='[\W\S]+?'
		pattern+='http://diesel\.elcat\.kg/index\.php\?showuser=(.+?)\"'

		result=re.search(pattern,data)

		if result == None:
			return 0
		else:
			return int(result.group(1))
			
	def GetNameById(self,id):
		response=self.__opener.open('http://diesel.elcat.kg/index.php?showuser='+str(id))
		data=response.read().decode('cp1251')

		if response.geturl()=='http://diesel.elcat.kg/index.php':
			return None

		pattern=u'<title>(.+?) - Просмотр профиля</title>'
		result=re.search(pattern,data)
		return result.group(1).encode('utf8')



	def UnLogin(self):
		response=self.__opener.open('http://diesel.elcat.kg')
		data=response.read().decode('cp1251')

		pattern=u'http://diesel\.elcat\.kg/index\.php\?act=Login&amp;CODE=03&amp;k=(.+?)">Выход'
		result=re.search(pattern,data)

		if result != None:
			self.__opener.open('http://diesel.elcat.kg/index.php?act=Login&CODE=03&k='+result.group(1))







	def SetRating(self,user,rating):
		if isinstance(user,int):
			return self.__setRatingById(user,rating)
		elif isinstance(user,basestring):
			return self.__setRatingById(self.GetIdByName(user),rating)
		else:
			return None
	def Login(self,login,password):
		login_data=urllib.urlencode({'UserName':login,'PassWord':password})
		self.__opener.open('http://diesel.elcat.kg/index.php?act=Login&CODE=01&CookieDate=1',login_data)

