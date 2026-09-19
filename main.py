from vector_engine import VectorDB

db = VectorDB(dense_mode=True)
db.index_documents(["PDFs/paper_dogs.pdf", "PDFs/paper_cats.pdf", "PDFs/paper_computers.pdf"])

answer = db.answer_query("what did the dog do")
print(answer)