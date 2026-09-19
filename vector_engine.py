from vectorMath import cosine_similarity as cs
from llm_client import generate_answer
from sentence_transformers import SentenceTransformer
import string
import pdfplumber


class VectorDB:
    def __init__(self, dense_mode=False):
        self.dense_mode = dense_mode # This is clearly what i need for better cosine similarity scores, bag of words wouldn't cut it 
        self.vocab_index = {}
        self.vectors = []
        self.registry = {}  # index -> [filename, raw_text]
        self.punctuation_set = set(string.punctuation) | {"“", "”", "…"}
        
        if self.dense_mode:
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2") # Loads once since it takes SOOO long to loaded across every method call

    def parser(self, list_of_pdfs):
        documents = []
        filenames = []

        for doc in list_of_pdfs:
            text_bucket = []
            with pdfplumber.open(doc) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text is None:
                        continue
                    text_bucket.append(text)

            full_text = " ".join(text_bucket)
            documents.append([full_text])
            filenames.append(doc.split("/")[1])

        return documents, filenames

    def tokenizer(self, documents=None):
        if documents is None:
            raise ValueError("Invalid data: Function parameters were empty")

        clean_docs = []
        for doc in documents:
            temp_doc = "".join(char for char in doc[0].lower() if char not in self.punctuation_set)
            clean_docs.append(temp_doc.split())

        return clean_docs

    def uniqueWords(self, tokenized_docs=None):
        if tokenized_docs is None:
            raise ValueError("Invalid data: Function parameters were empty")

        combined_docs = []
        for doc in tokenized_docs:
            combined_docs += doc

        return sorted(set(combined_docs))

    def build_vocab_index(self, vocab_list):
        self.vocab_index = {word: index for index, word in enumerate(vocab_list)}
        return self.vocab_index

    def vectorize(self, tokenized_docs):
        if tokenized_docs is None:
            raise ValueError("Invalid data: Function parameters were empty")

        all_vectors = []
        for doc in tokenized_docs:
            vector = [0] * len(self.vocab_index)
            for word in doc:
                if word in self.vocab_index:
                    vector[self.vocab_index[word]] += 1
            all_vectors.append(vector)

        return all_vectors

    def index_documents(self, list_of_pdfs):
        # Full ingestion pipeline: parse, tokenize, build vocab, vectorize, and register.
        documents, filenames = self.parser(list_of_pdfs)
        if self.dense_mode:
            raw_texts = [doc[0] for doc in documents]
            self.vectors = self.embedding_model.encode(raw_texts)
        else:
            tokenized = self.tokenizer(documents)
            vocab_list = self.uniqueWords(tokenized)
            self.build_vocab_index(vocab_list)
            self.vectors = self.vectorize(tokenized)

        self.registry = {
            index: [filenames[index], documents[index][0]]
            for index in range(len(filenames))
        }

    def search(self, query_text, cutoff=0.5):
        if query_text is None:
            raise ValueError("Please provide a query text.")
        
        if self.dense_mode:
            query_vector = self.embedding_model.encode(query_text)
        else:
            query_tokenized = self.tokenizer([[query_text]])
            query_vector = self.vectorize(query_tokenized)[0]

        results = {}
        for index, vector in enumerate(self.vectors):
            score = cs(query_vector, vector)
            if score >= cutoff:
                results[index] = {
                    "filename": self.registry[index][0],
                    "score": score
                }

        return results

db_dense_mode = VectorDB(dense_mode=True)
db = VectorDB(dense_mode=False)

pdf_paths = [
    "PDFs/paper_dogs.pdf",
    "PDFs/paper_cats.pdf",
    "PDFs/paper_computers.pdf"
]

db.index_documents(pdf_paths)
db_dense_mode.index_documents(pdf_paths)

print("Vocab size:", len(db.vocab_index))
print("Registry:", {k: v[0] for k, v in db.registry.items()})

print("\n--- Query: 'the dog ran around and played' ---")
results = db.search("the dog ran around and played", cutoff=0.0)
for index, info in results.items():
    print(index, info["filename"], round(info["score"], 3))

print("\n--- Query: 'cats sit and groom themselves' ---")
results = db.search("cats sit and groom themselves", cutoff=0.0)
for index, info in results.items():
    print(index, info["filename"], round(info["score"], 3))

print("\n--- Query: 'python code and databases' ---")
results = db.search("python code and databases", cutoff=0.0)
for index, info in results.items():
    print(index, info["filename"], round(info["score"], 3))

print("---------------------------------------------------------------------------------")

print("Vocab size:", len(db_dense_mode.vocab_index))
print("Registry:", {k: v[0] for k, v in db_dense_mode.registry.items()})

print("\n--- Query: 'the dog ran around and played' ---")
results = db_dense_mode.search("the dog ran around and played", cutoff=0.0)
for index, info in results.items():
    print(index, info["filename"], round(info["score"], 3))

print("\n--- Query: 'cats sit and groom themselves' ---")
results = db_dense_mode.search("cats sit and groom themselves", cutoff=0.0)
for index, info in results.items():
    print(index, info["filename"], round(info["score"], 3))

print("\n--- Query: 'python code and databases' ---")
results = db_dense_mode.search("python code and databases", cutoff=0.0)
for index, info in results.items():
    print(index, info["filename"], round(info["score"], 3))