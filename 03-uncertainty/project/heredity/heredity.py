import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                #p = joint_probability(people, {"Harry"}, {"James"}, {"James"})
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    names = set(people.keys())

    # initial joint probability
    joint_prob = 1

    for p in names:

        # gather parents' probabilities
        mother = people[p]['mother']
        father = people[p]['father']
        if mother in one_gene:
            # mother has one copy of the mutated gene, then she will pass 
            # the specific gene with probability 0.5
            # however, there's a chance the gene will modify (0.01)
            # so she can pass the mutated gene AND it mutate: 0.5 * 0.01, 
            # OR she doesnt pass the mutated gene AND it does not mutate: 0.5 *0.99 
            # which is just 0.5
            mother_prob = 0.5 
        elif mother in two_genes:
            # mother has prob of 1 - mutation
            # probability of getting the gene from mother:
            mother_prob = 1 - PROBS["mutation"]
        else:
            # mother has prob of 0 + mutation
            # the probability is just by mutation in this scenario
            mother_prob = PROBS["mutation"]
        
        if father in one_gene:
            father_prob = 0.5
        elif father in two_genes:
            father_prob = 1 - PROBS["mutation"]
        else:
            father_prob = PROBS["mutation"]

        if p in one_gene:
            # if no parent is listed:
            if people[p]['mother'] is None and people[p]['father'] is None: 
                prob = PROBS['gene'][1]
            else:
                # if p is a children, then it has a probability of receiving 
                # the gene from the parents

                # For someone to have EXACTLY 1 copy, then, the possiblities are either:
                # get from father AND not mother
                # OR 
                # get from mother AND not father
                prob = father_prob * (1 - mother_prob) + mother_prob * (1 - father_prob)
                
            no_trait = PROBS['trait'][1][False]
            trait = PROBS['trait'][1][True]
        elif p in two_genes:
            # if no parent is listed:
            if people[p]['mother'] is None and people[p]['father'] is None: 
                prob = PROBS['gene'][2]
            else:
                # if parent is listed
                
                # For someone to have EXACTLY 2 copies, then, the possiblities are only:
                # both mother and father pass the gene (recall it's already taking into account
                # the mutation in [mother/father]_prob)
                prob = mother_prob * father_prob

            no_trait = PROBS['trait'][2][False]
            trait = PROBS['trait'][2][True]

        else:
            if people[p]['mother'] is None and people[p]['father'] is None: 
                prob = PROBS['gene'][0]
            else:
                # if parent is listed

                # For someone to have EXACTLY 0 copies, then, the possiblities are only:
                # get 0 from mother AND 0 from father
                prob = (1-mother_prob) * (1-father_prob)

            no_trait = PROBS['trait'][0][False]
            trait = PROBS['trait'][0][True]

        if p in have_trait:
            final_trait = trait
        else:
            final_trait = no_trait

        joint_prob *= prob * final_trait

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    names = set(probabilities.keys())
    for person in names:
        if person not in one_gene and person not in two_genes:
            probabilities[person]['gene'][0] += p
        elif person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p

        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p

    return None


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    names = set(probabilities.keys())
    for person in names:
        
        trait_normalizer = 1 / sum(probabilities[person]['trait'].values())
        for item in probabilities[person]['trait'].keys():
            probabilities[person]['trait'][item] *= trait_normalizer

        gene_normalizer = 1 / sum(probabilities[person]['gene'].values())
        
        for item in probabilities[person]['gene'].keys():
            probabilities[person]['gene'][item] *= gene_normalizer

    return None


if __name__ == "__main__":
    main()
