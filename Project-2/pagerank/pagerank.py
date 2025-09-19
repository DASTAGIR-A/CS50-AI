import os
import random
import re
import sys

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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    links = corpus[page]
    if not links:
        links = set(corpus.keys())
    probab_dict = {}
    for p in corpus:
        if p in links:
            probab_dict[p] = (1 - damping_factor) / N + damping_factor / len(links)
        else:
            probab_dict[p] = (1 - damping_factor) / N
    return probab_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    track_dict ={}
    track_dict.update({page: 0 for page in corpus})
    random_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        track_dict[random_page] += 1
        transition_probabilities = transition_model(corpus, random_page, damping_factor)
        page = list(transition_probabilities.keys())
        weight = list(transition_probabilities.values())
        next_page = random.choices(page, weights= weight, k=1)[0]
        random_page = next_page
    page_rank = {key:val/n for key, val in track_dict.items()}
    return page_rank
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = {}
    threshold = 0.001

    # Initialize pagerank with equal probabilities
    for page in corpus:
        pagerank[page] = 1 / N

    converged = False

    while not converged:
        new_pagerank = {}

        for page in corpus:
            new_rank = (1 - damping_factor) / N
            total = 0

            for possible_linker in corpus:
                if page in corpus[possible_linker]:
                    total += pagerank[possible_linker] / len(corpus[possible_linker])
                elif not corpus[possible_linker]:
                    # Dangling page
                    total += pagerank[possible_linker] / N

            new_rank += damping_factor * total
            new_pagerank[page] = new_rank

        # Check for convergence AFTER all pages are updated
        converged = True
        for page in corpus:
            if abs(new_pagerank[page] - pagerank[page]) > threshold:
                converged = False
                break

        pagerank = new_pagerank.copy()

    return pagerank

if __name__ == "__main__":
    main()
