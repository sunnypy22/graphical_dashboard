import pandas as pd
import datetime as dt
import xml.etree.ElementTree as ET

xl_workbook = pd.ExcelFile('D:\\Logix\\Graphical Dashboard\\task-legal_sheet.xlsx')

# Sheet1 Data

sheet1 = xl_workbook.parse("sheet1-t_legal_status")

legal_status_id = sheet1['legal_status_id'].tolist()
publication_id = sheet1['publication_id'].tolist()
modified_load_id = sheet1['modified_load_id'].tolist()
status = sheet1['status'].tolist()
content = sheet1['content'].tolist()

# Sheet2 Data

sheet2 = xl_workbook.parse("sheet2- Abandoned")
Event_title = sheet2['Event-title'].tolist()

# Sheet3 Data

sheet3 = xl_workbook.parse("sheet3-Double")
sh3_title = sheet3['Event-title'].tolist()

# Sheet4 Data

sheet4 = xl_workbook.parse("Sheet4 ifi-integrated-content")
sh4_title = sheet4['content'].tolist()
sh4_publication_id = sheet4['publication_id'].tolist()

# Titles of sheet2
sheet2_list = []  # Title name from sheet2

for title in Event_title:
    sheet2_list.append(title)

# Titles of Sheet3
sheet3_list = []  # Title name from sheet3

for title in sh3_title:
    sheet3_list.append(title)



for sht4_test_xml in range(len(sh4_title)):
    root4 = ET.fromstring(sh4_title[sht4_test_xml])
    for neighbor in root4.iter('ifi-integrated-content'):
        print(neighbor.attrib)
    #     for k in neighbor.iter('ifi-patent-status-description'):
    #         print(k.text)
