import pandas as pd
import datetime as dt

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
    elif '<ifi-patent-status-description country="EP">' in ttle:
        index = ttle.index('<ifi-patent-status-description country="EP">')
        first_index = index + 44

        end_index = ttle.index('</ifi-patent-status -description>')
        final_val = ttle[first_index:end_index]
        COUNTRY_list.append(final_val)
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

import psycopg2

# conn = psycopg2.connect(dbname="mgpznpjc", user='mgpznpjc', password='pEuAWZjcHkTB86lDNLvMwTJKS-2l2aOw', host='satao.db.elephantsql.com', port='5432')
conn = psycopg2.connect(dbname="postgres", user='postgres', password='root', host='localhost', port='5432')
cursor = conn.cursor()


# for l in data:
#     cursor.execute(
#         "INSERT INTO test_task(date,legal_status_id,publication_id,modified_load_id,status,content) VALUES(%s, %s, %s, %s, %s, %s)"
#         , (
#             l['date'],
#             l['legal_status_id'],
#             l['publication_id'],
#             l['modified_load_id'],
#             l['status'],
#             l['content'],
#
#         ))
#     cursor.execute(
#         "INSERT INTO custome_tab(date,publication_id,status) VALUES(%s, %s, %s)"
#         , (
#             l['date'],
#             l['publication_id'],
#             l['status'],
#
#         ))

# sql = "COPY (SELECT * FROM test_task) TO STDOUT WITH CSV DELIMITER ';'"
# with open("D:\\Logix\\Graphical Dashboard\\data.csv", "w") as file:
#     cursor.copy_expert(sql, file)

# cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()

