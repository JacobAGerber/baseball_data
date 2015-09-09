import urllib2
from bs4 import BeautifulSoup
import re
from xml.dom import minidom
#import pdb; pdb.set_trace()


class Get_data:
	def __init__(self):
		pass


	def get_game_id(self, month, year):
		"""Given year & month, and day return which games happened"""
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
		'''Given a dictionary and columns list this function will sort a dictionary alphabetically
		--Deprecated 09/08/2015: Using ORM to load data
		'''
		self.columns = columns
		self.dict = dict
		for del_keys in dict.keys():
		#Parse elements and drop any keys that are not in columns checking dict which holds attributes
			if del_keys not in columns:
				del dict[del_keys]
		for final_keys in dict:
		#Combining all keys (columns) and checking to see if value is missing, coalesce to "cow."
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

	def column_filter(self, columns, dict):
		'''Given column list will ensure that dictionary only contains
		specified values
		'''
		self.columns = columns
		self.dict = dict
		for del_keys in dict.keys():
		#Parse elements and drop any keys that are not in columns checking dict which holds attributes
			if del_keys not in columns:
				del dict[del_keys]
		for final_keys in dict:
		#Combining all keys (columns) and checking to see if value is missing, coalesce to "missing"
			if final_keys not in dict.keys():
				dict[final_keys] = "missing"
		return dict
		
	
	def get_game_data(self, tagname, columns,month, year,link):
		'''Given an XML tagname, columns list, month & year for parsing, and list category  -- this function will return data to be written'''
		self.year = year
		self.month = month
		game_list = self.get_game_id(month, year)
		data_list = []
		for game in game_list:
			url = "http://gd2.mlb.com/components/game/mlb/year_" + str(game[0:4]) + '/month_' + str(game[5:7]) + '/day_' + str(game[8:10]) + '/gid_' + str(game) + '/' + link + '.xml' 
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
				data = self.column_filter(columns,values_dict)
				data['game_id'] = game
				data_list.append(data)
		return data_list
