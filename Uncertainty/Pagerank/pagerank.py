import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()

    # print(page)

    related_pages = corpus[page]
    if len(related_pages) == 0:
        related_pages.add(page)
    """ print(len(related_pages))
    print("huh") """
    dampProb = damping_factor / len(related_pages)
    prob = (1 - damping_factor) / len(corpus)
    for key in corpus.keys():
        if len(corpus[key]) == 0:
            model[key] = 1 / len(corpus)
        if key == page or key not in related_pages:
            model[key] = prob
        else:
            model[key] = prob + dampProb

    # print(model)
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    model = dict()

    for key in corpus:
        model[key] = 0.0

    firstSample = random.choice(list(corpus.keys()))
    model[firstSample] += 1 / n
    # print(firstSample)

    for i in range(1, n):
        # print("first sample: ", len(firstSample))
        probModel = transition_model(corpus, firstSample, damping_factor)
        keys = list(probModel.keys())
        prob = list(probModel.values())

        firstSample = random.choices(keys, weights=prob)[0]
        model[firstSample] += 1 / n
        # print("model stuff: ", model)

    # sum = 0.0
    # for values in model.values():
    # sum += values
    # print(sum)

    return model


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    model = dict()
    N = len(corpus)
    for key in corpus:
        model[key] = 1 / N

    done = False

    while not done:
        done = True
        copyModel = copy.deepcopy(model)
        for p in corpus:
            result = 0
            for i in corpus:
                if p in corpus[i]:
                    result += model[i] / len(corpus[i])

            model[p] = ((1 - damping_factor) / N) + (damping_factor * result)
            if abs(copyModel[p] - model[p] > 0.001):
                done = False

    return model


if __name__ == "__main__":
    main()
