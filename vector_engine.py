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

def uniqueWords(tokenized_docs=None):
    if tokenized_doc == None:
        raise ValueError("Invalid data: Function parameters were empty")
    
    combined_docs = []
    
    for doc in tokenized_docs:
        combined_docs += doc
    
    combined_docs = set(combined_docs)
    combined_docs = list(combined_docs)
    combined_docs.sort()
    
    return combined_docs

def build_vocab_index(vocab_list):
    return {word: index for index, word in enumerate(vocab_list)}

def vectorize(tokenized_docs, vocab_index):
    if tokenized_docs is None or vocab_index is None:
        raise ValueError("Invalid data: Function parameters were empty")

    all_vectors = []
    for doc in tokenized_docs:
        vector = [0] * len(vocab_index)   # blank vector, one slot per vocab word

        for word in doc:
            if word in vocab_index:
                index = vocab_index[word]
                vector[index] += 1        # count-based use = 1 instead for binary

        all_vectors.append(vector)

    return all_vectors

def search(query_text, all_vectors, vocab_index):
    if query_text == None or all_vectors == None or vocab_index == None:
        raise ValueError("Please provide a query text (User input) and make sure documents have been vectorized and slotted into this function alongisde the vocabulary index.")
    
    similarity_scores = {}
    
    query_tokenized = tokenizer([[query_text]])
    query_vector = vectorize(query_tokenized, vocab_index)[0]

    for index, vector in enumerate(all_vectors):
        cs_score = cs(query_vector, vector)
        similarity_scores[index] = cs_score
        
    return similarity_scores

def threshold(similarity_scores, cutoff=0.5):
    if similarity_scores == None:
        raise ValueError("Please make sure threshold parameters is provided... with a dictionary too.")
    
    filtered_scores = {}
    
    for index in similarity_scores:
        if similarity_scores[index] >= cutoff:
            filtered_scores[index] = similarity_scores[index]
            
    return filtered_scores


tokenized_doc = tokenizer([["the dog quickly, but slowly ran"], ["the cat, probably did sit."]])
vocab_words = uniqueWords(tokenized_doc)
vocab_index = build_vocab_index(vocab_words)
vectors = vectorize(tokenized_doc, vocab_index)
similarity_scores = search("the horse quickly ran across the field", vectors, vocab_index)
filtered_scores = threshold(similarity_scores)

print(tokenized_doc)
print(vocab_index)
print(vectors)
print(similarity_scores)
print(filtered_scores)