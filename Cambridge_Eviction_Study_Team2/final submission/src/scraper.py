

import os
from pageParser import PageParser
import csv

soup_parser = "lxml"


# --------------------------- SETUP AND CONNECT --------------------------- #

def main():

    directory = "./data"
    parse_files_nodb(directory)
    #conn.close()
    print("Done")



def parse_files_nodb(directory):
    print("Adding Files...")


    p_list=[]
    p_list.append(["Case Number", "Status", "FIle Date", "Plaintiff", "P-Attorney",  "Deffendant", "D-Attorney","Property Address", "Docket",
                   "Judgement Date", "Judgement Type", "JudgeMent Method", "Judgement Total", "Execution Total"])
    filepaths =[]

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".html"):
                #print(filepath)
                filepaths.append(filepath)

    for file in filepaths:
        with open(file, "rb") as fp:

            #print(directory + "/" + file)

            # Create parser object for page
            parser = PageParser(fp, soup_parser)

            # Parse document for case information
            res = parse_page_nodb(parser, file)
            if (res != None):
                p_list.append(res)


    #print(p_list)
    direct = "./csv"
    with open(direct + "/" +"dataFromDocket.csv", 'w') as f:
        csv.writer(f).writerows(p_list)

def parse_page_nodb(parser, file):
    res = []
    try:

        if parser.isCommercial():
            print("Skipping commercial case: " + file)
            return

        case_num = parser.get_case_num()
        res.append(case_num)
        status = parser.get_status()
        res.append(status)
        file_date = parser.get_file_date()
        res.append(file_date)
        plaintiff, defendant, plaintiffAtt, defendantAtt  = parser.get_parties('', '')

        res.append(plaintiff)
        res.append(plaintiffAtt)
        res.append(defendant)
        res.append(defendantAtt)

        property_addr = parser.get_address()
        res.append(property_addr)
        docket = parser.get_docket()
        res.append(docket)
        j_date, j_type, j_method = parser.get_judgement(status)
        res.append(j_date)
        res.append(j_type)
        res.append(j_method)
        j_total = parser.get_judgement_total()
        res.append(j_total)
        e_total = parser.get_execution_total(docket)
        res.append(e_total)
        
    except Exception as e:
         print("Unable to load data from file " + file + ": " + str(e))

    return res

# Call the program
main()
