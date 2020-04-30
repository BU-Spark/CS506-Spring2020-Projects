from PyPDF2 import PdfFileReader
import re
from tika import parser
import csv

def get_info(path):
    boas = re.compile("BOA[0-9]{6}")
    addresses = re.compile("Address:.*?[0-9A-Za-z,\n\-].*?Ward.*?[\n\-]+.*?[0-9]+")
    applicants = re.compile("Applicant:.*?[a-zA-Z\n]+.*?[A-Z][^A]*")

    raw = parser.from_file(path)
    boa_matches = boas.findall(raw['content'])
    address_matches = addresses.findall(raw['content'])
    applicant_matches = applicants.findall(raw['content'])
    print(boa_matches)
    print(address_matches)
    print(applicant_matches)
    print(len(boa_matches))
    print(len(address_matches))
    print(len(applicant_matches))

    newname = path[:-4]
    print(newname)
    with open(newname+".csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(boa_matches, address_matches, applicant_matches))


if __name__ == '__main__':
    path = '10_17_2017.pdf'
    get_info(path)