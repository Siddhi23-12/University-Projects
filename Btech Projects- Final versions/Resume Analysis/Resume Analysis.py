from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import spacy

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:

        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):

            # creating a resoure manager
            resource_manager = PDFResourceManager() 
      
            # create a file handle
fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

import spacy
from spacy.matcher import Matcher
# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('NAME', None, pattern)    
    matches = matcher(nlp_text)   
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        # print(span.text)
        return span.text

import re
def extract_mobile_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)   
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

import pandas as pd
def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    noun_chunks = nlp_text.noun_chunks

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop] 

    # reading the csv file
    data = pd.read_csv("skills.csv")  
   
    # extract values
    skills = list(data.columns.values)    
    skillset = []  
    # check for one-grams (example: python)

    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)   
    # check for bi-grams and tri-grams (example: machine learning)

    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)  
    return [i.capitalize() for i in set([i.lower() for i in skillset])]
from nltk.corpus import stopwords

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)
    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education
# file_path = 'Resume1.pdf'
file_path = 'Resume2.pdf'
text = ''
# calling above function and extracting text
for page in extract_text_from_pdf(file_path):
    text += ' ' + page

# print(text)
print('--------------Extracted information-----------------')
print('Name : ' + extract_name(text))
print('Mobile No. : ' + extract_mobile_number(text))
print('Email ID : ' + extract_email(text))
print('Education :\n', extract_education(text))
print('Skills :\n', extract_skills(text))
