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

	
def get_batter_boxscore_xml():
	
	save_path = 'C:\Python27\mlb_python'
	#Create batting file with boxscore
	bat_outfile_name = os.path.join(save_path,'mlbbatbox.csv')
	bat_outfile = open(bat_outfile_name, 'a')
	
	#Create CSV headers for writing (Batting)
	bat_headers = "game_id,batter_id,name,pos,bo,at_bats,po,runs,a,bb,sac,t,sf,hits,errors,d,hbp,so,hr,rbi,lob,fldg,sb"
	bat_outfile.write(bat_headers + "\n")	
	
	d_dates = get_dates.get_game_block_text('m',day='00',month='09',year='2012')
		
	for link in d_dates:
		print 'Gathering data for link: ' + '\n' + link + '\n'
		page_url = link + '/boxscore.xml'
		boxpage = urllib.urlopen(page_url)
		box = boxpage.read()
		for team in ("home","away"):
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
			
def get_pitcher_boxscore_xml():
	
	save_path = 'C:\Python27\mlb_python'
	#Create batting file with boxscore
	pitcher_outfile_name = os.path.join(save_path,'mlbpitchbox.csv')
	pitcher_outfile = open(pitcher_outfile_name, 'a')
	
	#Create CSV headers for writing (Pitching)
	pitch_headers = "game_id,pitcher_id,name,pos,bf,er,runs,hits,so,hr,bb,np,s,win,loss,save,hold,blown_save"
	pitcher_outfile.write(pitch_headers + "\n")
	
	d_dates = get_dates.get_game_block_text('m',day='00',month='09',year='2012')
	
	for link in d_dates:
		print 'Gathering data for link: ' + '\n' + link + '\n'
		page_url = link + '/boxscore.xml'
		boxpage = urllib.urlopen(page_url)
		box = boxpage.read()
		for team in ("home","away"):
			print team
			# #Count of batters for looping
			pitching_start = box.find("<pitching team_flag=\"" + team) + 9
			pitching_end = box.find("/pitching",pitching_start) - 12
			pitching = box[pitching_start:pitching_end]
			pitching_count = pitching.count("pitcher id")
			print 'Pitcher Count ' + str(pitching_count)
			game_location = [m.start() for m in re.finditer(r"pitcher id",pitching)]
			print 'Pitching Count Index ' + str(len(game_location))
			for g in game_location:
				start = g
				end = pitching.index('/p',start)
				pitcher_stats = pitching[start:end] + '\n'
				pitcher_id = statFind("pitcher id",pitcher_stats)
				name = statFind(" name_display_first_last",pitcher_stats)
				pos = statFind(" pos",pitcher_stats)
				out = statFind(" out",pitcher_stats)
				bf = statFind(" bf",pitcher_stats)
				er = statFind(" er",pitcher_stats)
				runs = statFind(" r",pitcher_stats)
				hits = statFind(" h",pitcher_stats)
				so = statFind(" so",pitcher_stats)
				hr = statFind(" hr",pitcher_stats)
				bb = statFind(" bb",pitcher_stats)
				np = statFind(" np",pitcher_stats)
				s = statFind(" s",pitcher_stats)
				win = statFind(" win",pitcher_stats)
				if win == "true":
					win = 1
				loss = statFind(" loss",pitcher_stats)
				if loss == "true":
					loss = 1
				save = statFind(" save",pitcher_stats)
				if save == "true":
					save = 1
				hold = statFind(" hold",pitcher_stats)
				if hold == "true":
					hold = 1
				blown_save = statFind(" blown_save",pitcher_stats)
				if blown_save =="true":
					blown_save = 1
				pitch_row = link + "," + pitcher_id + "," + name + "," + pos + "," + bf + "," + er + "," + runs + "," + hits + "," + so + "," + hr + "," + bb + "," + np + "," + s + "," + str(win) + "," + str(loss) + "," + str(save) + "," + str(hold) + "," + str(blown_save)
			
			pitcher_outfile.write(pitch_row + "\n")


get_batter_boxscore_xml()
get_pitcher_boxscore_xml()
