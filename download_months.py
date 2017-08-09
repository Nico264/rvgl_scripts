#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import tkinter.filedialog

import beautifulscraper as bs
import zipfile
import os

parser = argparse.ArgumentParser(description='Download latest month tracks')

parser.add_argument('--path', type=str, help='Path where Re-Volt/RVGL is located.')

args = parser.parse_args()

rvgl_dir = args.path if args.path else tkinter.filedialog.askdirectory()

os.chdir(rvgl_dir)

scrapper = bs.BeautifulScraper()
webpage = scrapper.go("https://www.revoltrace.net/month_tracks.php")

os.mkdir("temp")

for a in webpage.find_all(attrs={"class": "downloadTrack"}):
    url = bs.urlparse(a.get("href"))
    if url.netloc == "revoltzone.net":
        track_id = url.path.split("/")[2]
        inter_url = "http://revoltzone.net/sitescripts/dload.php?id="+track_id
        inter = bs.urllib2.urlopen(inter_url)
        
        true_url = inter.getheader("Location")
        track_name = url.path.split("/")[3]
    if url.netloc == "revoltxtg.co.uk":
        true_url = url.geturl()
        track_name = url.geturl().split("/")[-1][:-4]
    
    print("Downloading from "+true_url)
    true_url = true_url[:8]+bs.quote(true_url[8:])
    bs.urllib2.urlretrieve(true_url, "./temp/"+track_name+".zip")

for filename in os.listdir("temp"):
    print("Extracting "+filename)
    
    file_uri = './temp/'+filename
    with zipfile.ZipFile(file_uri, "r") as z:
        z.extractall()
    os.remove(file_uri)

os.rmdir("temp")

if os.name == "posix":
    os.execv("./fix_cases", ("./fix_cases",))

exit(0)
