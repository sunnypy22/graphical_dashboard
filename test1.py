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

def get_key(val,dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"

for title in Event_title:
    sheet2_list.append(title)

# Titles of Sheet3
sheet3_list = []  # Title name from sheet3

for title in sh3_title:
    sheet3_list.append(title)



sht4_val = []
for sht4_test_xml in range(len(sh4_title)):
    root4 = ET.fromstring(sh4_title[sht4_test_xml])

    for neighbor in root4.iter('ifi-integrated-content'):
        for k in neighbor.iter('ifi-patent-status-description'):
            sht4_val.append({
                'value': k.text,
                'pb': sh4_publication_id[sht4_test_xml]

            })
            break



date_title = []
pub_dt = {}
for test_xml in range(len(content)):
    root = ET.fromstring(content[test_xml])
    ttl_dt = []

    for neighbor in root.iter('legal-event'):

        str_date = neighbor.attrib['date']
        date_append = str_date[0:4] + "-" + str_date[4:6] + "-" + str_date[6:8]
        d = dt.datetime.strptime(date_append, "%Y-%m-%d")
        d = d.date()
        # print(d)

        date_title = []

        for k in neighbor.iter('event-title'):
            ttl_dt.append({
                'date': d,
                'title': k.text,

            })
            date_title.append(ttl_dt)

        pub_dt[publication_id[test_xml]] = date_title

# Update date_title for Date Format (String to Date)

for values in pub_dt.values():
    values[0].sort(key=lambda x: x['date'])
    values[0] = values[0][::-1]

for j in pub_dt.values():
    if j[0][0]['title'] in sheet2_list:
        j[0].append({
            'status': "Abandoned"
        })

    elif j[0][0]['title'] in sheet3_list:
        j[0].append({
            'status': "Double"
        })
    else:
        pub_id = get_key(j,pub_dt)
        for m in sht4_val:
            z = m['pb']
            if pub_id == z:
                j[0].append({
                    'status': m['value']
                })
