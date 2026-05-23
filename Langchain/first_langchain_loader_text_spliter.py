from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import ArxivLoader
from langchain_community.document_loaders import WikipediaLoader

from langchain_text_splitters  import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

test  = TextLoader('notes.txt')

print(test.load())

test2 = PyPDFLoader('sample-1.pdf')

print(test2.load())

test3 = WebBaseLoader('https://www.geeksforgeeks.org/artificial-intelligence/large-language-model-llm/')

print(test3.load())

test4 = ArxivLoader(query = '1706.03762')

print(test4.load())

test5 = WikipediaLoader(query = 'AI Agents', load_max_docs = 1)

print(test5.load())

splitter = PyPDFLoader('sample-1.pdf')

fulltext = splitter.load()

print(fulltext)

full_text_split = "\n".join([doc.page_content for doc in fulltext])

print(full_text_split)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=100, chunk_overlap=0)

texts = text_splitter.split_text(fulltext)

print(texts)

text_splitter2 = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)

text2 = text_splitter2.split_text([fulltext])