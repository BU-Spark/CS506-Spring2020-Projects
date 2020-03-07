#   scraper.py
#
#   By: Deanna Baris
#   Date: 4/30/18
#
#   This script takes a directory of raw html pages saved from the
#   Massachusetts Trial Court Electronic Case Access site. The
#   case information from each page is parsed and added to a
#   Microsoft Access Database.
#
#   To run on Windows:      py -3 -m scraper <data/YEAR/MONTH>

import os
import sys
import pyodbc
from pageParser import PageParser

soup_parser = "lxml"


# --------------------------- SETUP AND CONNECT --------------------------- #

def main():

    # Check that user provides files to scrape
    # if (len(sys.argv) != 2):
    #     print("Usage: py -3 -m scraper <data/YEAR/MONTH>")
    #     exit(1)
    #
    # directory = sys.argv[1]
    # print(directory==r'data/2019/Jan')
    directory = r'data/2019/Jan'

    # Connect to Access Database
    driver = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; '

    # Database Location
    db = r'DBQ=C:\Users\CT-2.0\Desktop\Ca\eviction-data.accdb;'
    conn, c = access_connect(driver, db)
    print("Connected to database")

    parse_files(directory, c, conn)
    conn.close()
    print("Done")


#   Connect to Microsoft Access database
def access_connect(driver, db):
    try:
        conn_str = (driver + db)
        conn = pyodbc.connect(conn_str)
        c = conn.cursor()
        return (conn, c)
    except Exception:
        print("Unable to connect to database")
        raise


# Convert db response tuples to list
def dbToList(query, c):
    c.execute(query)
    response_tuples = c.fetchall()
    new_list = []

    for r in response_tuples:
        if r[0] is None:
            continue
        new_list.append(r[0])

    return new_list


#   Parse all html files within directory and store in database
def parse_files(directory, c, conn):
    print("Adding Files...")

    # Get list of existing plaintiffs & defendants
    p_list = dbToList("""SELECT DISTINCT plaintiff FROM evictions""", c)
    d_list = dbToList("""SELECT DISTINCT defendant FROM evictions""", c)

    # Add information for all files in provided directory
    for file in os.listdir(directory):
        with open(directory + "/" + file, "rb") as fp:
            # Create parser object for page
            parser = PageParser(fp, soup_parser)

            # Parse document for case information
            p_list, d_list = parse_page(parser, file, c, conn, p_list, d_list)


def parse_page(parser, file, c, conn, p_list, d_list):
    try:
        case_num = parser.get_case_num()

        # If resolved case not in database, add it (no duplicates)
        sql = "SELECT case_id from evictions WHERE case_id=\'" + \
              case_num + "\' AND [status]<>'Open'"
        c.execute(sql)
        response = c.fetchall()

        if response == []:
            # Exclude commercial properties
            if parser.isCommercial():
                print("Skipping commercial case: " + file)
                return p_list, d_list

            # Parse the rest of the case data
            status = parser.get_status()
            file_date = parser.get_file_date()
            plaintiff, defendant = parser.get_parties(p_list, d_list)
            property_addr = parser.get_address()
            docket = parser.get_docket()
            j_date, j_type, j_method = parser.get_judgement(status)
            j_total = parser.get_judgement_total()
            e_total = parser.get_execution_total(docket)
            unit, s_num, s_name, s_type = parser.parse_address(property_addr)

            if j_date == "":
                j_date = None

            if defendant not in d_list:
                d_list.append(defendant)

            if plaintiff not in p_list:
                p_list.append(plaintiff)

            if j_type is "" and j_date is "" and j_method is "":
                print("Judgement not found for file: " + file +
                      ". Please add manually. ")
                return p_list, d_list

            # Check for any open entries
            sql = "SELECT * from evictions WHERE case_id=\'" + \
                case_num + "\' AND [status]='Open'"
            c.execute(sql)
            response = c.fetchall()

            #  Remove any previous open entries, replace with resolved
            if response != []:
                sql = "DELETE FROM evictions WHERE case_id=\'" + \
                       case_num + "\' AND [status]='Open'"
                c.execute(sql)
                conn.commit()

            # Insert case
            print("Inserting case: " + case_num)
            sql = "INSERT INTO evictions (case_id, status, file_date, \
                judgement_date, plaintiff, defendant, property_addr, \
                judgement_type, judgement_method, docket, \
                judgement_total, unit, street_number, street_name, \
                street_type, execution_total) values \
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            c.execute(sql, case_num, status, file_date, j_date,
                      plaintiff, defendant, property_addr, j_type,
                      j_method, docket, j_total, unit, s_num, s_name,
                      s_type, e_total)

            conn.commit()

        # Skip duplicate resolved cases
        else:
            print("Case %s already in database" % (case_num,))

        return p_list, d_list

    except Exception as e:
        print("Unable to load data from file " + file + ": " + str(e))


# Call the program
main()
