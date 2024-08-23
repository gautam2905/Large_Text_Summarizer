from transformers import pipeline 
import warnings
from test_box import GUI
from transformers import AutoTokenizer
from langchain_text_splitters import NLTKTextSplitter

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

warnings.filterwarnings("ignore")

def word_count(data):
    return len(data.split())


article = GUI()
article = tokenizer.backend_tokenizer.normalizer.normalize_str(article)

summary = summarizer(article, max_length=200, min_length=30, do_sample=False)

text_splitter = NLTKTextSplitter(chunk_size=3072)
texts = text_splitter.split_text(article)

summary=""
for i in range(len(texts)):
    data = tokenizer.backend_tokenizer.normalizer.normalize_str(texts[i])
    sum_temp = summarizer(data, min_length = int(0.1 * len(data)), max_length = int(0.2 * len(data)), do_sample=False)
    summary += sum_temp[0]["summary_text"]

ff = open('summary.txt','w+')
ff.write(summary)

# print(f" {len(article)} , {len(summary[0]["summary_text"])}")


