import math

def dot_product(vector_a, vector_b):
    if vector_a is None or vector_b is None:
        raise ValueError("Must insert in specifically 2 vectors of the same length in the function")
    
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must be the same length.")
    
    total = 0
    
    for i in range(len(vector_a)):
        total += vector_a[i] * vector_b[i]
        
    return total

def magnitude(vector=None):
    if vector is None:
        return 0
    
    total = 0
    
    for i in range(len(vector)):
        total += vector[i] ** 2
    
    return math.sqrt(total)

def cosine_similarity(vector_a, vector_b):
    if vector_a is None or vector_b is None:
        raise ValueError("Must insert in 2 vectors")
    
    numerator = dot_product(vector_a, vector_b)
    denominator = magnitude(vector_a) * magnitude(vector_b)
    
    if denominator == 0:
        raise ValueError(f"Please do not insert in the 0 vector, it breaks the cosine similarity method")
    
    return numerator / denominator


if __name__ == "__main__":
    print("-- Running test --")
    
    # Test for dot_product()
    result = dot_product([1, 2, 3], [4, 5, 6])
    print(f"Testing Dot Product: [1, 2, 3] * [4, 5, 6], Expected 32, Got {result}")
    assert result == 32
    
    # Test for magnitude()
    result = magnitude([3,4])
    print(f"Testing Magnitude: [3, 4], Expected 5, Got {result}")
    assert result == 5.0
    
    # Test for cosine_similarity()

    # Case 1: same direction -> 1.0
    result = cosine_similarity([3, 4], [6, 8])
    print(f"Testing Cosine Similarity (same direction): [3,4] vs [6,8], Expected 1.0, Got {result}")
    assert result == 1.0

    # Case 2: orthogonal (90 degrees apart) -> 0.0
    result = cosine_similarity([3, 4], [4, -3])
    print(f"Testing Cosine Similarity (orthogonal): [3,4] vs [4,-3], Expected 0.0, Got {result}")
    assert result == 0.0

    # Case 3: opposite direction -> -1.0
    result = cosine_similarity([3, 4], [-3, -4])
    print(f"Testing Cosine Similarity (opposite direction): [3,4] vs [-3,-4], Expected -1.0, Got {result}")
    assert result == -1.0

    # Case 4: zero vector should raise ValueError
    try:
        cosine_similarity([0, 0], [1, 1])
        print("Testing Cosine Similarity (zero vector): FAILED - no exception raised")
    except ValueError as e:
        print(f"Testing Cosine Similarity (zero vector): Correctly raised - {e}")