from vectorMath import cosine_similarity as cs

class VectorDB: # Going to soon sort this into a class for reusability for different projects
    def __init__(self):
        pass
    
    
def tokenizer(document=None):
    if document == None:
        raise ValueError("Invalid data: Function parameters were empty")
    
    punctuation_set = {"!", "?", ",", ".", "'"} # I am aware there are a lot of punctuation in UNICODE im just using a few for testing
    clean_doc = "".join(char for char in document if char not in punctuation_set)
    clean_doc = clean_doc.lower().split()
    
    return clean_doc


output = tokenizer("Hello, I'm having, hmm... quite a nice day today!")

print(output)