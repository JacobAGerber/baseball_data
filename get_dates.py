#!/usr/bin/python


import urllib
import urllib2
import datetime
import sys
import getopt
import os.path
from bs4 import BeautifulSoup
import re
import os
import requests
from requests.exceptions import HTTPError



def statFind(stat_tag,block_text):
	stat_start = block_text.find(stat_tag + "=") + len(stat_tag) + 2
	stat_end = block_text.find("\"",stat_start)
	if stat_start - len(stat_tag) - 2 == -1:
		stat = 0
	else:
		stat = block_text[stat_start:stat_end]
	return str(stat)
	
def get_game_id(url):
	g_id = [a.text.strip()[4:-1] for a in BeautifulSoup(urllib2.urlopen(url)).find_all('li',text=re.compile("gid_"))]
	return g_id
	
def get_year(year):


	"""When provided with year will return all game IDs available"""
	y = year
	fullurl = 'http://gd2.mlb.com/components/game/mlb/year_' + y
	m_id = []
	d_id = []
	g_id = []
	m_id = [a.text.strip()[4:-1] for a in BeautifulSoup(urllib2.urlopen(fullurl)).find_all('li',text=re.compile("month_"))]
	for m in m_id:
		get_day = fullurl + '/month_' + m[-2:]
		d_id = [d.text.strip()[4:-1] for d in BeautifulSoup(urllib2.urlopen(get_day)).find_all('li',text=re.compile("day_"))]
		for d in d_id:
			url = get_day + '/day_' + d[-2:]
			print m[-2:] +'/'+ d +'/' + y
	return g_id			

def get_month(month, year):
	"""When provided with month & year will return all game IDs available"""
	y = year
	m = month
	url = 'http://gd2.mlb.com/components/game/mlb/year_' + y + '/month_' + m
	d_id = []
	g_id = []
	d_id = [d.text.strip()[4:-1] for d in BeautifulSoup(urllib2.urlopen(url)).find_all('li',text=re.compile("day_"))]
	"""For each day (d or d_id) in a month cycle through and find game ids per day"""
	for d in d_id:
		day_url = url + '/day_' + d[-2:]
		a = get_game_id(day_url)
		g_id.append(a)
	return g_id		

def get_day(day, month, year):
	"""When provided with month & year and date will return all game IDs available for specific day"""
	y = year
	m = month
	d = day
	fullurl = 'http://gd2.mlb.com/components/game/mlb/year_' + y + '/month_' + m + '/day_' + d
	g_id = []
	g_id = [a.text.strip()[4:-1] for a in BeautifulSoup(urllib2.urlopen(fullurl)).find_all('li',text=re.compile("gid_"))]

def platform():
	while 1:
		#os.system('cls')
		print("Baseball Platform")
		print("")
		print("1. Import Year")
		print("2. Get Import Month")
		print("3. Get Day")
		print("4. Get Player")
		print("5. Exit")
		choice = raw_input("Enter a choice: ")
		if choice == "1":
			#os.system('cls')
			try:
				get_year()
				os.system('cls')
			except:
				os.system('cls')
				print 'Error'
		elif choice == "2":
			#os.system('cls')
			try:
				get_month()
			except:
				os.system('cls')
				print 'Error'
			#os.system('cls')
		elif choice == "3":
			try:
			#os.system('cls')		
				get_day()
			except:
				os.system('cls')
				print 'Error'
			#os.system('cls')		
		elif choice == "4":
			#os.system('cls')	
			pass
			#os.system('cls')		
		elif choice == "5":
			os.system("cls")
			break;

def get_game_details():
	error_log = []
	a = get_month('08','2012')
	for g in a:
		for i in g:
			year, month, day = i[0:4], i[5:7], i[8:10]
			url = 'http://gd2.mlb.com/components/game/mlb/year_' + year + '/month_' + month + '/day_' + day + '/gid_' + i
			try:
				open = urllib2.urlopen(url)
				cow = BeautifulSoup(open)
			except:
				error_log.append(url)
	if error_log > 0:
		print error_log
	else:
		pass
			
get_game_details()
