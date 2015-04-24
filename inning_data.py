#!/usr/bin/python


import urllib, urllib2,datetime,sys,getopt,os.path,re,os,requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import get_dates
import re


def statFind(stat_tag,block_text):
	stat_start = block_text.find(stat_tag + "=") + len(stat_tag) + 2
	stat_end = block_text.find("\"",stat_start)
	if stat_start - len(stat_tag) - 2 == -1:
		stat = 0
	else:
		stat = block_text[stat_start:stat_end]
	return str(stat)

	
def get_inning_data():
	
	save_path = 'C:\Python27\mlb_python'
	#Create batting file with boxscore
	bat_outfile_name = os.path.join(save_path,'mlbbatbox.csv')
	bat_outfile = open(bat_outfile_name, 'a')
	
	#Create CSV headers for writing (Batting)
	bat_headers = "game_id,batter_id,name,pos,bo,at_bats,po,runs,a,bb,sac,t,sf,hits,errors,d,hbp,so,hr,rbi,lob,fldg,sb"
	bat_outfile.write(bat_headers + "\n")	
	
	d_dates = get_dates.get_game_block_text('m',day='00',month='09',year='2012')
		
	for link in d_dates:
		#print 'Gathering data for link: ' + '\n' + link + '\n'
		page_url = link + '/inning/inning_all.xml'
		boxpage = urllib.urlopen(page_url)
		box = boxpage.read()
		inning_location = [m.start() for m in re.finditer(r'inning num',box)]
		inning_total = len(inning_location)
		for inning in range(1, inning_total + 1):
			print inning
			inning_start = box.find("<inning num=\"" + str(inning) ) 
			inning_end = box.find('/inning',inning_start) 
			inning_split = box[inning_start:inning_end]
			at_bat_location = [m.start() for m in re.finditer(r"atbat num",inning_split)]
			for at_bat_seq in at_bat_location:
				bat_start = inning_split.find("<atbat num")
				bat_end = inning_split.find("/atbat",bat_start)
				bat_details = inning_split[bat_start:bat_end]
				
		
