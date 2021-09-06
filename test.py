import pandas as pd
import datetime as dt
import xml.etree.ElementTree as ET

xl_workbook = pd.ExcelFile('D:\\Logix\\Graphical Dashboard\\task-legal_sheet.xlsx')

#  Parameters

# sh1 = "sheet1-t_legal_status"
# sh2 = "sheet2- Abandoned"
# sh3 = "sheet3-Double"
# sh4 = "Sheet4 ifi-integrated-content"
#
# sh1_pb = "publication_id"
# sh4_pb = "publication_id"
#
# sh1_content = "content"
# sh2_content = "Event-title"
# sh3_content = "Event-title"
# sh4_content = "content"


# database connection
def db_conn():
    import psycopg2
    conn = psycopg2.connect(dbname="mgpznpjc", user='mgpznpjc', password='pEuAWZjcHkTB86lDNLvMwTJKS-2l2aOw',
                            host='satao.db.elephantsql.com', port='5432')
    return conn


# Read Excel File
def read_sheet(sheet_name):
    sheet = xl_workbook.parse(sheet_name)
    return sheet


# Read publication id from excel
def read_pb_id(sht_name, pb_id):
    sheet1 = read_sheet(sht_name)
    pb_id = sheet1[pb_id].tolist()
    return pb_id


# read title from excel
def content(sht_name, content):
    sheet1 = read_sheet(sht_name)
    content = sheet1[content].tolist()
    return content


# Return key name from dictionary from related value
def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"


sheet2_list = []  # Title name from sheet2
sheet3_list = []  # Title name from sheet3
sht4_val = []  # Title name from sheet4

for title in content("sheet2- Abandoned", "Event-title"):  # Titles of Sheet2
    sheet2_list.append(title)

for title in content("sheet3-Double", "Event-title"):  # Titles of Sheet3
    sheet3_list.append(title)

for sht4_test_xml in range(len(content("Sheet4 ifi-integrated-content", "content"))):  # Titles of Sheet4
    root4 = ET.fromstring(content("Sheet4 ifi-integrated-content", "content")[sht4_test_xml])

    for neighbor in root4.iter('ifi-integrated-content'):
        for k in neighbor.iter('ifi-patent-status-description'):
            sht4_val.append({
                'value': k.text,
                'pb': read_pb_id("Sheet4 ifi-integrated-content", "publication_id")[sht4_test_xml]
            })
            break

date_title = []
pub_dt = {}  # Store date and title in dict format
for test_xml in range(len(content("sheet1-t_legal_status", "content"))):
    root = ET.fromstring(content("sheet1-t_legal_status", "content")[test_xml])
    ttl_dt = []

    for neighbor in root.iter('legal-event'):

        str_date = neighbor.attrib['date']
        date_append = str_date[0:4] + "-" + str_date[4:6] + "-" + str_date[6:8]
        d = dt.datetime.strptime(date_append, "%Y-%m-%d")
        d = d.date()

        date_title = []

        for k in neighbor.iter('event-title'):
            ttl_dt.append({'date': d, 'title': k.text, })
            date_title.append(ttl_dt)

        pub_dt[read_pb_id("sheet1-t_legal_status", "publication_id")[test_xml]] = date_title

# Update date_title for Date Format (String to Date)

for values in pub_dt.values():
    values[0].sort(key=lambda x: x['date'])
    values[0] = values[0][::-1]

# Condition for data availability in sheet2, sheet3 and sheet4

for j in pub_dt.values():
    if j[0][0]['title'] in sheet2_list:
        j[0].append({'status': "Abandoned"})

    elif j[0][0]['title'] in sheet3_list:
        j[0].append({'status': "Double"})

    else:
        pub_id = get_key(j, pub_dt)
        for m in sht4_val:
            z = m['pb']
            if pub_id == z:
                j[0].append({'status': m['value']})

conn = db_conn()
cursor = db_conn().cursor()
for final_data in pub_dt.values():
    fnl_data = final_data[0]
    date = final_data[0][0]['date']
    pub_id = get_key(final_data, pub_dt)
    try:
        sts = fnl_data[-1]['status']
        cursor.execute("INSERT INTO test_task(Date,pub_id,status) VALUES(%s, %s, %s)", (date, pub_id, sts,))
        conn.commit()
    except:
        sts = 'V'
        cursor.execute("INSERT INTO test_task(Date,pub_id,status) VALUES(%s, %s, %s)", (date, pub_id, sts,))
        conn.commit()
cursor.close()
conn.close()