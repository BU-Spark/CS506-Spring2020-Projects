import pandas as pd 
import PyPDF2

def read_pdf(filename):
  pdf_file = open(filename,'rb')
  read_pdf = PyPDF2.PdfFileReader(pdf_file)
  number_of_pages = read_pdf.getNumPages()

  state_agencies = []
  for i in range(number_of_pages):
    page = read_pdf.getPage(i)
    page_content = page.extractText()
    page_content = page_content.split('\n')
    state_agencies.append(page_content)

  return state_agencies

"""filters mapc dataset by land use code, poly-type, and lots with buildings

accepted_codes = ['910','911','912','913','914','915','916','917','918','919','920','921','922',
				 '923','924','925','926','927','928','929','970','971','972','973','974','975']

df = pd.read_pickle(/Users/taylorhazlett/Documents/spring2020/cs506/mapc.pkl)


df = filter_luc(df)
df = filter_poly_typ(df)
df = filer_bldg(df)
"""

print(read_pdf('state_agency_names.pdf'))
