from xml.dom import minidom
import xml.etree.ElementTree as ET 
import json

annFile = "681_sampled_politician_video.xml"
parentFol = "framewise_sampled_annotations/"
#"""
# parse an xml file by name
mydoc = minidom.parse(annFile)

print(mydoc)

tracks = mydoc.getElementsByTagName('track')

for elem in tracks:
	print(elem.attributes['label'].value)

# total amount of items
print(len(tracks))
finalann = {}
for i in range(len(tracks)):
	if (tracks[i].attributes['label'].value == "face"):
		boxes = tracks[i].getElementsByTagName('box')
	
		for elem in boxes:
			frameNum = elem.attributes["frame"].value
			outside = elem.attributes["outside"].value
			if outside == "0":
				annDict = {}
				annDict["xmax"] = elem.attributes["xbr"].value
				annDict["ymax"] = elem.attributes["ybr"].value
				annDict["xmin"] = elem.attributes["xtl"].value
				annDict["ymin"] = elem.attributes["ytl"].value
				ann = elem.getElementsByTagName('attribute')
				for a in ann:
					annDict[a.attributes['name'].value] = a.childNodes[0].data


				if frameNum in finalann:
					finalann[frameNum].append(annDict)
				else:
					finalann[frameNum] = [annDict]


print(finalann)

for k in finalann.keys():
	f = open( parentFol + k + ".json", "w")
	json.dump(finalann[k], f)
	f.close()
