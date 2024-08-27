from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
from gui_maker import *
import re
import string
import en_core_web_sm
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import spacy
import numpy as np
from wordsegment import load, segment
load()

def word_seprator(text):
    lis = segment(sum)
    return " ".join(lis)

text = GUI()
bart_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
bart_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

nlp = spacy.load('en_core_web_sm')

def clean_string(text, stem="Spacy"):

    final_string = ""

    # Make lower
    text = text.lower()

    # Remove line breaks
    # Note: that this line can be augmented and used over
    # to replace any characters with nothing or a space
    text = re.sub(r'\n', '', text)

    # Remove punctuation
    # translator = str.maketrans('', '', string.punctuation)
    # text = text.translate(translator)

    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']

    text_filtered = [word for word in text if not word in useless_words]

    # Remove numbers
    text_filtered = [re.sub(r'\w*\d\w*', '', w) for w in text_filtered]

    # Stem or Lemmatize
    if stem == 'Stem':
        stemmer = PorterStemmer() 
        text_stemmed = [stemmer.stem(y) for y in text_filtered]
    elif stem == 'Lem':
        lem = WordNetLemmatizer()
        text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    elif stem == 'Spacy':
        text_filtered = nlp(' '.join(text_filtered))
        text_stemmed = [y.lemma_ for y in text_filtered]
    else:
        text_stemmed = text_filtered

    final_string = ' '.join(text_stemmed)

    return final_string

text = clean_string(text,None)
# word_count(text)

def nest_sentences(document):
  nested = []
  sent = []
  length = 0
  for sentence in nltk.sent_tokenize(document):
    length += len(sentence)
    if length < 1024:
      sent.append(sentence)
    else:
      nested.append(sent)
      sent = []
      length = 0

  if sent:
    nested.append(sent)
  return nested

# generate summary on text with <= 1024 tokens
def generate_summary(nested_sentences):
  # device = 'cuda'
  summaries = []
  for nested in nested_sentences:
    input_tokenized = bart_tokenizer.encode(' '.join(nested), truncation=True, return_tensors='pt')
    # input_tokenized = input_tokenized.to(device)
    summary_ids = bart_model.generate(input_tokenized,
                                      length_penalty=3.0,
                                      min_length=30,
                                      max_length=100)
    output = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    summaries.append(output)
  summaries = [sentence for sublist in summaries for sentence in sublist]
  final_string = ""
  final_string =  ' '.join(summaries)
  return final_string

senn = nest_sentences(text)
summ = generate_summary(senn)
summ = word_seprator(text)

f = open("summary.txt",'w+')
f.write(sum)
f.close()
