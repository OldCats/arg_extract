from bs4 import BeautifulSoup
from glob import glob
import pandas as pd

def list_xmls():
    dirs = glob('*_batch_*')

    xmls = []
    for dir in dirs:
        xmls += glob(dir+'/*')

    return xmls


def convert_xml_to_list(xml):
    row = {}
    rows = []
    row['articleId'] = xml
    row['file_type'] = 'xml'

    # open file
    f = open(xml, 'r', encoding='utf-8')
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    sections = ['abstract', 'intro']

    for section in sections:
        para = soup.findChild(section).findAll('p')

        for p in para:

            row['Section'] = section
            row['p'] = p.attrs['id']

            ss = []
            ss.extend(p.findChildren('s'))

            for s in ss:
                try:
                    row['s'] = s.attrs['id']
                except:
                    row['s'] = ''
            
                args = []
                args.extend(s.findChildren('arg'))

                for arg in args:
                    row['text'] = arg.text
                    new_row = row.copy()
                    new_row.update(arg.attrs)
                    rows.append(new_row)
    return rows


def start():
    xmls = list_xmls()
    output = pd.DataFrame()

    for xml in xmls:
        print(xml)
        xml_list = convert_xml_to_list(xml)

        df = pd.DataFrame(xml_list)
        
        output = pd.concat([output, df])

    output.to_excel('output.xlsx')

if __name__ == '__main__':
    start()