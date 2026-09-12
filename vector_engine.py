from vectorMath import cosine_similarity as cs

class VectorDB: # Going to soon sort this into a class for reusability for different projects
    def __init__(self):
        pass
    
    
def tokenizer(documents=None):
    if documents == None:
        raise ValueError("Invalid data: Function parameters were empty")
    
    clean_doc = []
    
    punctuation_set = {"!", "?", ",", ".", "'"} # I am aware there are a lot of punctuation in UNICODE im just using a few for testing
    
    for doc in documents:
        temp_doc = ["".join(char for char in word.lower() if char not in punctuation_set) for word in doc]
        temp_doc = temp_doc[0].split()
        clean_doc.append(temp_doc)
    
    return clean_doc

def uniqueWords(tokenized_text):
    combined_docs = []
    
    for doc in tokenized_text:
        combined_docs += doc
    
    combined_docs = set(combined_docs)
    combined_docs = list(combined_docs)
    combined_docs.sort()
    
    return combined_docs

output = tokenizer([["Hello, I'm having, hmm... quite a nice day today!"], ["I think I am Lebron James' son, back in 05 when he was ballin'! his life out."]])

print(output)