from xml.dom import minidom
import urllib
import get_dates
import os
import csv

failed_links = []

save_path = 'C:\Python27\mlb_python'
#Create batting file with boxscore
file_name = os.path.join(save_path,'pitch_detail_box.csv')
pitch_outfile = open(file_name, 'a')


d_dates = get_dates.get_month('08','2012')

for g_id_list in d_dates:
		for link in g_id_list:
			try:
				print "Opening Game: " + link
				url = "http://gd2.mlb.com/components/game/mlb/year_" + str(link[0:4]) + '/month_' + str(link[5:7]) + '/day_' + str(link[8:10]) + '/gid_' + str(link) + '/inning/inning_all.xml'
				url = urllib.urlopen(url) 
				xml_data = minidom.parse(url)
				xml_data_inning = xml_data.getElementsByTagName('atbat')
			except:
				print "Failed Link: " + link
				failed_links.append(link)
			for at_bats in xml_data_inning:
				at_bat_data = at_bats.getElementsByTagName('pitch')
				at_bat_items = ['num','b','s','o','batter','stand','b_height','pitcher','p_throws','event']
				at_bat_dict = (dict(at_bats.attributes.items()))
				for del_keys in at_bat_dict.keys():
					if del_keys not in at_bat_items:
						del at_bat_dict[del_keys]
				dict_copy = at_bat_dict.copy()
				for pitch_data in at_bat_data:
					pitch_items = ['id','type','x','y','start_speed','sz_top','sz_bot','pfx_x','pfx_z','px','pz','x0','y0','z0','vx0','vy0','vz0','ax','ay','az','break_y','break_angle','break_lenght','zone','spin_dir','spin_rate']
					pitch_dict = (dict(pitch_data.attributes.items()))
					for del_keys_p in pitch_dict.keys():
						if del_keys_p not in pitch_items:
							del pitch_dict[del_keys_p]
					pitch_dict_c = pitch_dict
				dict_copy.update(pitch_dict_c)
				pitch_outfile.write(str(dict_copy.values()).lstrip('u') + "\n")
					
pitch_outfile.close()
