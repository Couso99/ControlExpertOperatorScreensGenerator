
tags_fname = "FILTERED_TAGS/TP06_EXPORT_TP06.txt"
screenName = "Screen_TP06"
outfname = "OPERATOR_SCREENS/"+screenName+".XCR"

#For telling inputs and outputs apart. Can be left blank.
keyWordsForOutputs = ["_CO", "VauxOK", "CFR", "CFV", "_HC", "_FC", "_CR", ".DEFECTO"]

intro = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<SCRExchangeFile>
	<fileHeader company="Schneider Automation" product="Control Expert V15.0 - 201016B" dateTime="date_and_time#2022-5-9-15:27:35" content="Operator Screen source file" DTDVersion="41"></fileHeader>
	<contentHeader name="Project" version="0.0.3" dateTime="date_and_time#2022-5-6-15:41:35"></contentHeader>
	<IOScreen version="V1.0">
		<screen name="{screenName}" screenX="1280" screenY="1024" BKColor="-1" valScreen="0" location="" creationDate="06/05/2022 - 12:20:03" modificationDate="09/05/2022 - 15:27:26" customInfos="" isPattern="0" valPattern="0">
'''

outro = '''</screen>
</IOScreen>
</SCRExchangeFile>
'''

def get_position(x,y,cx,cy):
    return f"({y},{x},{y+cy},{x+cx})"

def objectInputBool(varName, position):
    return f'''<object objectID="18" description="{position},(-1,0,0,1),|{varName}|">
        <varPilot name="{varName}" typeName="BOOL" description="Pilot:|0|0|"></varPilot>
    </object>
    '''

def objectOutputBool(varName, position):
    return 	f'''<object objectID="2" description="{position},2"></object>
    <object objectID="15" description="{position},(0,1,0),(11,0,255),|{varName}|Calibri|,(10,1,0,0,0,0,0)">
        <varAnim name="{varName}" typeName="BOOL" description="Anim:0,|-|-|,(0,0),(0,0)"></varAnim>
    </object>
    <object objectID="15" description="{position},(0,1,0),(11,0,65280),|{varName}|Calibri|,(10,1,0,0,0,0,0)">
        <varAnim name="{varName}" typeName="BOOL" description="Anim:2,|-|-|,(0,0),(0,0)"></varAnim>
    </object>
    '''

def objectInputEbool(varName, position):
    return f'''<object objectID="18" description="{position},(-1,0,0,1),|{varName}|">
        <varPilot name="{varName}" typeName="EBOOL" description="Pilot:|0|0|"></varPilot>
    </object>
    '''

def objectOutputEbool(varName, position):
    return 	f'''<object objectID="2" description="{position},2"></object>
    <object objectID="15" description="{position},(0,1,0),(11,0,255),|{varName}|Calibri|,(10,1,0,0,0,0,0)">
        <varAnim name="{varName}" typeName="EBOOL" description="Anim:0,|-|-|,(0,0),(0,0)"></varAnim>
    </object>
    <object objectID="15" description="{position},(0,1,0),(11,0,65280),|{varName}|Calibri|,(10,1,0,0,0,0,0)">
        <varAnim name="{varName}" typeName="EBOOL" description="Anim:2,|-|-|,(0,0),(0,0)"></varAnim>
    </object>
    '''

def objectOutputInt(varName, position1, position2, position3):
    return f'''<object objectID="2" description="{position3},2"></object>
    <object objectID="15" description="{position1},(0,1,0),(10,0,255),|{varName}|Calibri|,(10,0,0,0,0,0,0)"></object>
    <object objectID="21" description="{position2},(0,1,1,0)">
        <varPilot name="{varName}" typeName="INT" description="Pilot:|0|5|"></varPilot>
    </object>
    '''

def get_variables(fname):
    tags = []
    with open(fname, 'r') as f:
        rows = f.readlines()
    for row in rows:
        tags.append(row.split('\t\t')[0:2])
	#
    if '¿' in tags[0][0]:
        tags[0][0] = tags[0][0].split('¿')[1]
    return tags


tags = get_variables(tags_fname)
tags.sort()

xStart = 10
yStart = 10

#For booleans
cxBool = 165
cyBool = 40

#For integers objects
cxInt1 = cxBool
cxInt2 = cxBool
cyInt1 = 18
cyInt2 = cyBool - cyInt1

#Spacing between objects
cxBlank = 10
cyBlank = 5

number_of_rows = 12
row_counter = 0
column_counter = 0

tags_string = ""

for tag in tags:
	if "BOOL" in tag[1]:
		#Go through the keyWordsForOutputs to tell apart from inputs
		if any([x in tag[0] for x in keyWordsForOutputs]):
			if "EBOOL" in tag[1]:
				tags_string += objectOutputEbool(tag[0],get_position(xStart+column_counter*(cxBool+cxBlank),yStart+row_counter*(cyBool+cyBlank),cxBool,cyBool))
			else:
				tags_string += objectOutputBool(tag[0],get_position(xStart+column_counter*(cxBool+cxBlank),yStart+row_counter*(cyBool+cyBlank),cxBool,cyBool))
		else:
			if "EBOOL" in tag[1]:
				tags_string += objectInputEbool(tag[0],get_position(xStart+column_counter*(cxBool+cxBlank),yStart+row_counter*(cyBool+cyBlank),cxBool,cyBool))
			else:
				tags_string += objectInputBool(tag[0],get_position(xStart+column_counter*(cxBool+cxBlank),yStart+row_counter*(cyBool+cyBlank),cxBool,cyBool))

		row_counter += 1
		if row_counter == number_of_rows:
			row_counter = 0
			column_counter += 1
	elif "INT" in tag[1]:
		pos1 = get_position(xStart+column_counter*(cxInt1+cxBlank),yStart+row_counter*(cyInt1+cyInt2+cyBlank),cxInt1,cyInt1)
		pos2 = get_position(xStart+column_counter*(cxInt1+cxBlank),yStart+row_counter*(cyInt1+cyInt2+cyBlank)+cyInt1,cxInt2,cyInt2)
		pos3 = get_position(xStart+column_counter*(cxInt1+cxBlank),yStart+row_counter*(cyInt1+cyInt2+cyBlank),cxInt1,cyInt1+cyInt2)
		tags_string += objectOutputInt(tag[0], pos1, pos2, pos3)

		row_counter += 1
		if row_counter == number_of_rows:
			row_counter = 0
			column_counter += 1

	else:
		print(f"Datatype not implemented. Skipping to next tag. (objeto: {tag})\n")
		continue

final_str = intro + tags_string + outro

with open(outfname,"w") as f:
    f.write(final_str)
