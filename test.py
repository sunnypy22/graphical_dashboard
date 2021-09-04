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

    # Title Name

COUNTRY_list = []
for ttle in sh4_title:
    if '<ifi-patent-status-description country="US">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="US">')
        first_index = index + 44

        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="AU">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="AU">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="CA">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="CA">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="JP">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="JP">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="ES">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="ES">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="DE">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="DE">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="FR">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="FR">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="GB">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="GB">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    # elif '<ifi-patent-status-description country="EP">' in ttle:
    #     index = ttle.index('<ifi-patent-status-description country="EP">')
    #     first_index = index + 44
    #
    #     end_index = ttle.index('</ifi-patent-status -description>')
    #     final_val = ttle[first_index:end_index]
    #     COUNTRY_list.append(final_val)
    elif '<ifi-patent-status-description country="CN">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="CN">')
        first_index = index + 44
        end_index = ttle.index('</ifi-patent-status-description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
    else:
        COUNTRY_list.append('Nothing')

sht_4_data = []
for data in range(len(sh4_publication_id)):
    sht_4_data.append({
        'publication_id': sh4_publication_id[data],
        'title_value': COUNTRY_list[data]
    })

title_check = []  # Add to Status Field
for title_eve in content:
    if "<event-title>" in title_eve:
        index = title_eve.index('<event-title>')
        first_index = index + 13
        end_index = title_eve.index('</event-title>')
        final_title = title_eve[first_index:end_index]
        if final_title in sheet2_list:
            title_check.append('Abandoned')
        elif final_title in sheet3_list:
            title_check.append('Double')
        else:
            title_check.append('v')
    else:
        title_check.append('Null')

date_field = []
for date in content:
    index = date.index('date')
    first_idex = index + 6
    last_index = index + 14
    date_append = date[first_idex:first_idex + 4] + "-" + date[first_idex + 4:first_idex + 6] + "-" + date[
                                                                                                      first_idex + 6:first_idex + 8]
    date_str = date[first_idex:last_index]
    d = dt.datetime.strptime(date_append, "%Y-%m-%d")
    d = d.date()
    date_field.append(d)

sorted_date = sorted(date_field)

data = []
for i in range(len(date_field)):
    data.append(
        {
            'legal_status_id': legal_status_id[i],
            'publication_id': publication_id[i],
            'modified_load_id': modified_load_id[i],
            'status': title_check[i],
            'content': content[i],
            'date': date_field[i]
        }
    )

# print(data)
data.sort(key=lambda x: x['date'])
data = data[::-1]

for i in data:
    if i['status'] == "Null":
        pb_id = i['publication_id']
        for k in range(len(sht_4_data)):
            if sht_4_data[k]['publication_id'] == pb_id:
                i['status'] = sht_4_data[k]['title_value']

import xml.etree.ElementTree as ET

# date_list = []
# for date in range(len(content)):
#     root = ET.fromstring(content[date])
#     date = []
#     for child in root:
#         date_str = child.attrib['date']
#
#         date.append({
#             'date': date_str
#         })
#     date_list.append(date)

id = []
for test_xml in range(len(content)):
    root = ET.fromstring(content[test_xml])
    if "legal-status" in root.tag:
        date = []
        for child in root:
            date_str = child.attrib['date']

            date.append({
                'date': date_str
            })
        title = []
        for neighbor in root.iter('event-title'):
            append_title = neighbor.text
            if append_title in sheet2_list:
                status = "Abandoneone"
            elif append_title in sheet3_list:
                status = "Double"
            else:
                status = "v"
            title.append(
                {
                    "title": append_title,
                    "status": status,
                    "date": date
                }
            )
        id.append(
            {
                'pb_id': publication_id[test_xml],
                'title': title,
            }
        )
date_title = []
for test_xml in range(len(content)):
    root = ET.fromstring(content[test_xml])
    ttl_dt = []
    for neighbor in root.iter('legal-event'):

        str_date = neighbor.attrib['date']
        date_append = str_date[0:4] + "-" + str_date[4:6] + "-" + str_date[6:8]
        d = dt.datetime.strptime(date_append, "%Y-%m-%d")
        d = d.date()
        # print(d)

        for k in neighbor.iter('event-title'):
            ttl_dt.append({
                'date': neighbor.attrib['date'],
                'title': k.text
            })
    date_title.append(ttl_dt)
        # print(neighbor.attrib['date'])


# Date Format (String to Date)

for view in date_title:
    view[0]['date'] = view[0]['date'][0:4] + "-" + view[0]['date'][4:6] + "-" + view[0]['date'][6:8]
    db = view[0]['date']
    date_format = dt.datetime.strptime(db, "%Y-%m-%d")
    finl_dt_date = date_format.date()
    view[0]['date'] = finl_dt_date

for test_xml in range(len(content)):
    root = ET.fromstring(content[test_xml])
    ttl_dt = []
    for neighbor in root.iter('legal-event'):
        for k in neighbor.iter('event-title'):
            print(k.tag)
