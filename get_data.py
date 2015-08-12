from xml.dom import minidom
import urllib2
from bs4 import BeautifulSoup
import re
from xml.dom import minidom

class Get_data:
	
	def __init__(self):
		pass
	

	def get_game_id(self, month, year):
		"""Given year & month, and day return which games happened at specific time"""
		games = []
		self.month = str(month)
		self.year = str(year)
		link = 'http://gd2.mlb.com/components/game/mlb/year_' + self.year + '/month_' + self.month
		day = [d.text.strip()[4:-1] for d in BeautifulSoup(urllib2.urlopen(link)).find_all('li',text=re.compile("day_"))]
		try:
			for d in day:
				url = link + '/day_' + d
				g_id = [a.text.strip()[4:-1] for a in BeautifulSoup(urllib2.urlopen(url)).find_all('li',text=re.compile("gid_"))]
				for g in g_id:
					games.append(g)
		finally:
			return games
		
	
	def dict_key_sort(self, columns, dict):
		self.columns = columns
		self.dict = dict
		for del_keys in dict.keys():
		# #Parse elements and drop any keys that are not in columns checking dict which holds attributes
			if del_keys not in columns:
				del dict[del_keys]
		for final_keys in dict:
		# #Combining all keys (columns) and checking to see if value is missing, coalesce to "cow."
			if final_keys not in dict.keys():
				dict[final_keys] = "cow"
		cow = sorted(dict)
		#Arbitrary Name
		cow_values = []
		cow_values_list = []
		for key_list in cow:
			if key_list in dict.keys():
				cow_values = dict.values()[dict.keys().index(key_list)]
				cow_values_list.append(cow_values)
		return cow_values_list
	
	
	def get_game_data(self, tagname, columns,month, year, file_name='default'):
		self.year = year
		self.month = month
		game_list = self.get_game_id(month, year)
		fname = open('C:\\Python27\\''' + file_name + '.csv', 'w')
		for game in game_list:
			url = "http://gd2.mlb.com/components/game/mlb/year_" + str(game[0:4]) + '/month_' + str(game[5:7]) + '/day_' + str(game[8:10]) + '/gid_' + str(game) + '/boxscore.xml' #LINK (FIGURE OUT ARG)
			try:
				url = urllib2.urlopen(url) 
				xml_data = minidom.parse(url)
				xml_data_tag = xml_data.getElementsByTagName(tagname)
				print 'Parsed: ' + game
			except:
				print 'Failed to Open Link: ' + url
				continue
			for game_details in xml_data_tag:
				values_dict = (dict(game_details.attributes.items()))
				data = self.dict_key_sort(columns,values_dict)
				fname.write("|".join(map(str,data)) + "\n")
