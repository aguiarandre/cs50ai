import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 200000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks_sample = ranks.copy()
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks_iterate = ranks.copy()

    print(sum([abs(ranks_iterate[k] - ranks_sample[k]) for k in ranks.keys()]))


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
    all_pages = set(corpus.keys())

    # create a dictionary to store results
    pages = {}
    for k in all_pages:
        pages[k] = 0
    
    # with probability 1 - damping_factor, choose randomly from all_pages
    spread_probability = (1 - damping_factor) / len(all_pages)
    # with probability `damping_factor`, choose from current links in page
    domain_size = len(corpus[page]) or len(corpus)
    keep_probability = damping_factor / domain_size

    for each_page in all_pages:
        pages[each_page] += spread_probability
        if each_page in corpus[page]:
            pages[each_page] += keep_probability

    # corpus[page] are the pages I have 
    return pages

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    Random Surfer Model
    """
    all_pages = list(corpus.keys())

    # create a dictionary to store results
    pages = {}
    for k in all_pages:
        pages[k] = 0

    # select randomly from the set of pages
    page = random.choice(all_pages)
    for _ in range(n):
        tm = transition_model(
            corpus=corpus, 
            page=page, 
            damping_factor=damping_factor
        )
        # get 1 sample for the next page given the pages probabilities
        page = random.choices(
            population=all_pages, 
            weights=[tm[p] for p in all_pages], 
            k=1
        )[0]
        
        pages[page] += 1/n

    return pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    eps = 1e-3
    counter = 0
    all_pages = list(corpus.keys())
    N = len(all_pages)
    # create a dictionary to store results
    # pages will be the initial pagerank (prev)
    pagerank_storage = {}
    # pagerank will be the resulting pagerank after an iteration (after)
    pagerank = {}
    for k in all_pages:
        pagerank_storage[k] = 1 / N
        pagerank[k] = 1 / N

    # with probability 1 - d, the surfer chose a page at random 
    # and ended up on page p.
    random_surf = (1 - damping_factor) / N
    
    converged = False
    while not converged:
        for p in all_pages:
            # A page that has no links at all should be interpreted 
            # as having one link for every page in the corpus (including itself).
            if corpus[p] == set():
                corpus[p] = set(all_pages)

            # we need to loop through all the pages that links to p
            links_to_p = set()
            for l in all_pages:
                if p in corpus[l]:
                    links_to_p.add(l)
    
            link_surf = 0
            # with probability d, the surfer followed a link from 
            # a page i to page p.
            for i in links_to_p:
                # domain size is the number of links present in page i
                domain_size = len(corpus[i])
                
                # pagerank[i] represents the probability that we are
                # on page i and surf to p
                
                # divide by the number of pages in page i (because from there,
                # you could move to every page with the same probability)
                link_surf += damping_factor * pagerank[i] / domain_size

                # note that using pagerank (instead of previous pagerank value 
                # stored in pagerank_storage) increases the convergence rate.

            pagerank[p] = random_surf + link_surf

        if convergence_criterion(pagerank_storage, pagerank, eps, 'Linf'):
            converged = True

        counter += 1
        pagerank_storage = pagerank.copy()
    return pagerank


def convergence_criterion(prev, after, eps, norm='L2'):
    if norm not in ('L1','L2','Linf'):
        raise NotImplementedError('Convergence criteria not implemented yet.')
    
    if norm == 'L1':
        # L1 norm is the mean-absolute-error
        if sum([abs(prev[p] - after[p]) for p in prev.keys()]) < eps:
            return True
    if norm == 'L2':
        if sum(([(prev[p] - after[p])**2 for p in prev.keys()]))**1/2 < eps:
            return True
    if norm == 'Linf':
        if max([abs(prev[p] - after[p]) for p in prev.keys()]) < eps:
            return True

    return False

if __name__ == "__main__":
    main()
