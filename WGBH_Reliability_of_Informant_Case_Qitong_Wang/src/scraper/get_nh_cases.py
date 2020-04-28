import os
import re
import csv
import json
import pdftotext
# sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
# pip3 install pdftotext


def get_nh_cases(path, year_start, year_end):
    pdfnames_cases = extract_cases(path, year_start, year_end)
    cases_data = []
    for pdf_case in pdfnames_cases:
        pdf_name = pdf_case[0]
        case_text = pdf_case[1]
        case_text_no_newline = [p.replace('\n', ' ') for p in case_text]

        case = {'file name': pdf_name, 'title': "N/A", 'type': "N/A", 'decision': "N/A",
                'text': case_text_no_newline}

        if not (len(case_text) == 1
                or "modified" in pdf_name
                or "caption" in pdf_name
                or "order" in pdf_name.lower()):

            # locate header
            p_header = find_paragraph(case_text, ["_________"])
            # locate Submitted or Argued date
            p_submitted_argued = find_paragraph(case_text, ["Submitted: "])
            if p_submitted_argued == -1:
                p_submitted_argued = find_paragraph(case_text, ["Argued: "])
            # locate Opinion Issued date
            p_opinion_issued = find_paragraph(case_text, ["Opinion Issued: "])
            # locate case decision
            decisions = ['affirmed', "reversed", "vacated", "remanded", "dismissed", "ordered", "denied"]
            case_text_lowercase = [p.lower() if "\n" not in p else "" for p in case_text]
            p_decision = len(case_text) - 1 - find_paragraph(case_text_lowercase[::-1], decisions)
            if p_decision == len(case_text):
                case_text_lowercase = [paragraph.lower().split("\n")[0] for paragraph in case_text]
                p_decision = len(case_text) - 1 - find_paragraph(case_text_lowercase[::-1], decisions)

            # get case title
            if not (p_header == -1 or p_submitted_argued == -1):
                case['title'] = ' '.join(case_text_no_newline [p_header + 1:p_submitted_argued])
            # get case type
            if not p_opinion_issued == -1:
                case['type'] = find_criminal(case_text_no_newline[p_opinion_issued + 3].split(' '), pdf_name)
            # get case decision
            if p_decision != len(case_text):
                decision = case_text_no_newline[p_decision].split("\n")[0]
                if "affirmed in part" in decision.lower():
                    case['decision'] = "affirmed in part"
                elif "affirm" in decision.lower():
                    case['decision'] = "affirmed"
                else:
                    case['decision'] = "not affirmed"

        cases_data.append(case)
    return cases_data


def extract_cases(path, year_start, year_end):
    pdfnames_cases = []
    for year in range(year_start, year_end + 1):
        # read file names in this year
        filenames = os.listdir(path + "/" + str(year))
        # load pdf files
        for filename in filenames:
            # excluding non-pdf files
            if filename.endswith('.pdf'):
                # get pdf object and extract text from pdf object
                with open(path + "/" + str(year) + "/" + filename, "rb") as f:
                    pdf_obj = pdftotext.PDF(f)
                pdf = remove_page_number(pdf_obj)
                text = ''.join(pdf)
                # record reading errors
                if text:
                    paragraphs = re.split(r'\s{2,}', text)
                    pdfnames_cases.append([filename, paragraphs])
    # return pdf files in a list of [pdfname, case]
    return pdfnames_cases


def remove_page_number(pdf_obj):
    pdf = []
    for page in pdf_obj:
        if page:
            line = page.rsplit("\n", 2)
            if line[1].strip().isdigit():
                pdf.append(line[0] + "\n")
            else:
                pdf.append(page)
    return pdf


def find_paragraph(case_text, keywords):
    for n, paragraph in enumerate(case_text):
        for keyword in keywords:
            if keyword in paragraph:
                return n
    return -1  # if keyword not found


def find_criminal(headnote, pdf_name):
    for n, word in enumerate(headnote):
        # according to RSA document in NH https://www.gencourt.state.nh.us/rsa/html/nhtoc.htm
        # CRIMINAL CODE is included in TITLE LXII including chapter 625 - 651-f
        rsa_num = -1
        if word == 'RSA': # find the number after appearance of  RSA
            if re.search('\d', headnote[n + 1]):
                try:
                    rsa_num = int(re.findall('\d+', headnote[n + 1])[0])
                except ValueError:
                    print(headnote[n + 1][:3] + " after RSA " + pdf_name)
            elif re.search('\d', headnote[n + 2]):
                try:
                    rsa_num = int(re.findall('\d+', headnote[n + 2])[0])
                except ValueError:
                    print(headnote[n + 2][:3] + " after RSA " + pdf_name)
        if 625 <= rsa_num < 652:
            return 'criminal'
    return 'non-criminal'


def save_result(path, fmt, cases):
    if fmt == "json":
        # write to a json file
        with open(path + '/cases_nh.json', 'w') as fout:
            json.dump(cases, fout)
    elif fmt == "csv":
        # write to a csv file
        keys = cases[0].keys()
        with open(path + '/cases_nh.csv', 'w') as fout:
            dict_writer = csv.DictWriter(fout, keys)
            dict_writer.writeheader()
            dict_writer.writerows(cases)
    else:
        print("Invalid format")


if __name__ == "__main__":

    # read from ../pdf_nh_cases
    pdf_nh_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pdf_nh_cases"
    # get cases from 2008 to 2018
    nh_cases = get_nh_cases(pdf_nh_path, 2008, 2018)

    # save to ../data
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data"
    # save as json or csv
    save_result(save_path, "json", nh_cases)





