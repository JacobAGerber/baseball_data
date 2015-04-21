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

	
def get_boxscore_xml():
	
	save_path = 'C:\Python27\mlb_python'
	#Create batting file with boxscore
	bat_outfile_name = os.path.join(save_path,'mlbbatbox.csv')
	bat_outfile = open(bat_outfile_name, 'a')
	
	#Create CSV headers for writing (Batting)
	bat_headers = "game_id,batter_id,name,pos,bo,at_bats,po,runs,a,bb,sac,t,sf,hits,errors,d,hbp,so,hr,rbi,lob,fldg,sb"
	bat_outfile.write(bat_headers + "\n")	
	
	d_dates = get_dates.get_game_block_text('m',day='00',month='08',year='2012')
		
	
	for link in d_dates:
		print 'Gathering data for link: ' + '\n' + link
		page_url = link + '/boxscore.xml'
		boxpage = urllib.urlopen(page_url)
		box = boxpage.read()
		for team in ("home","away"):
			print team
			# #Count of batters for looping
			batting_start = box.find("<batting team_flag=\"" + team) + 9
			batting_end = box.find("/batting",batting_start) - 12
			batting = box[batting_start:batting_end]
			batter_count = batting.count("batter id")
			print 'Batter Count ' + str(batter_count)
			game_location = [m.start() for m in re.finditer(r"batter id",batting)]
			print 'Batter Count Index ' + str(len(game_location))
			for g in game_location:
				start = g
				end = batting.index('/batter',start)
				batters = batting[start:end] + '\n'
				
				batter_id = statFind("batter id",batters)
				name = statFind(" name_display_first_last",batters)
				print "Batter Name: " + name
				pos = statFind(" pos",batters)
				bo = statFind(" bo",batters)
				at_bats = statFind(" ab",batters)
				po = statFind(" po",batters)
				runs = statFind(" r",batters)
				a = statFind(" a",batters)
				bb = statFind(" bb",batters)
				sac = statFind(" sac",batters)
				t = statFind(" t",batters)
				sf = statFind(" sf",batters)
				hits = statFind(" h",batters)
				errors = statFind(" e",batters)
				d = statFind(" d",batters)
				hbp = statFind(" hbp",batters)
				so = statFind(" so",batters)
				hr = statFind(" hr",batters)
				rbi = statFind(" rbi",batters)
				lob = statFind(" lob",batters)
				fldg = statFind(" fldg",batters)
				sb = statFind(" sb",batters)	
				bat_row = link + "," + batter_id + "," + name + "," + pos + "," + bo + "," + at_bats + "," + po + "," + runs + "," + a + "," + bb + "," + sac + "," + t + "," + sf + "," + hits + "," + errors + "," + d + "," + hbp + "," + so + "," + hr + "," + rbi + "," + lob + "," + fldg + "," + sb
				#write to csv
				bat_outfile.write(bat_row + '\n')
			

				
get_boxscore_xml()
