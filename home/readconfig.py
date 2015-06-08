import sys,os  
import ConfigParser  
  
class readconfig:  
	def __init__(self, config_file_path):  
		cf = ConfigParser.ConfigParser()  
		cf.read(config_file_path)
		
		s = cf.sections()  
		#print 'section:', s  
	  
		o = cf.options("baseconf")  
		#print 'options:', o  
	  
		v = cf.items("baseconf")  
		#print 'db:', v  
	  
		self.db_host = cf.get("baseconf", "host")  
		self.db_port = cf.getint("baseconf", "port")  
		self.db_user = cf.get("baseconf", "user")  
		self.db_pwd = cf.get("baseconf", "password")
		self.db_name = cf.get("baseconf", "db_name")
		#print self.db_host, self.db_port, self.db_user, self.db_pwd  		

	def gethost(self):
		return self.db_host
		
	def getport(self):
		return self.db_port
		
	def getuser(self):
		return self.db_user
	
	def getpwd(self):
		return self.db_pwd
		
	def getdb(self):
		return self.db_name