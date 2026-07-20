from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize stop words and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess(text):
    """
    Preprocess the input text by:
    1. Converting to lowercase
    2. Tokenizing
    3. Removing punctuation
    4. Removing stop words
    5. Lemmatizing words
    """

    # Convert to lowercase
    text = text.lower()

    # Tokenize the sentence
    tokens = word_tokenize(text)

    # Store processed words
    processed_words = []

    # Remove stop words and punctuation, then lemmatize
    for word in tokens:
        if word.isalpha() and word not in stop_words:
            processed_words.append(lemmatizer.lemmatize(word))

    return processed_words


# Test the function
if __name__ == "__main__":
    sentence = input("Enter a sentence: ")
    result = preprocess(sentence)
    print("\nProcessed Output:")
    print(result)