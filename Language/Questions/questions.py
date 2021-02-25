import nltk
import sys
import os
import math
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding="utf8") as f:
            content = f.read()
            files[filename] = content
    
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    words = nltk.word_tokenize(document)

    filtered_words = []
    stopwords = set(nltk.corpus.stopwords.words("english"))
    punctuation = set(string.punctuation)

    for word in words:
        if word not in stopwords and word not in punctuation:
            filtered_words.append(word)

    return filtered_words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    totalDoc = len(documents)
    allWords = set()
    for file in documents:
        allWords.update(set(documents[file]))

    for word in allWords:
        num = 0
        # sum(word in documents[filename] for filename in documents)
        for file in documents.values():
            if word in file:
                num += 1
        idf = math.log(totalDoc / num)
        idfs[word] = idf
    
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    #print(query)
    #print(files.items())
    for file, words in files.items():
        tfidf = 0
        for word in query:
            tfidf += (files[file].count(word) * idfs[word])
        tfidfs[file] = tfidf

    # print(tfidfs)

    sorted_tfidfs = sorted(tfidfs.items(), key=lambda k: (k[1]), reverse=True)
    # print(sorted_tfidfs)
    sorted_tfidfs = [file[0] for file in sorted_tfidfs]
    # print(sorted_tfidfs)

    return sorted_tfidfs[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    matchingWordMeasure = dict()
    for sentence, words in sentences.items():
        total = 0
        density = 0
        for word in query:
            if word in sentences[sentence]:
                density += 1
                total += idfs[word]
        density = float(density) / len(words)
        matchingWordMeasure[sentence] = (total, density)
    
    #print(matchingWordMeasure.items())
    sorted_measure = sorted(matchingWordMeasure.items(), key=lambda k: (k[1][0], k[1][1]), reverse=True)
    # print(sorted_measure[:n])
    sorted_measure = [sentence[0] for sentence in sorted_measure]
    # print(sorted_measure[:n])

    return sorted_measure[:n]

if __name__ == "__main__":
    main()
