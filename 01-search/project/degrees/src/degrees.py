import csv
import sys

from util import Node, StackFrontier, QueueFrontier

from tqdm.auto import tqdm

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    # source = person_id_for_name("Demi Moore")
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    # target = person_id_for_name("Emma Watson")
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def while_generator():
    while True:
        yield

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    initial_state = source # state is the person_id
    explored_set = set()
    # variable used to verify success condition
    goal_check = False 
    # add source node to frontier
    node = Node(state=initial_state, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(node)
    iteration_number = 0

    # while True:
    for _ in tqdm(while_generator(), desc='Searching ...'):

        iteration_number+=1
        # check if frontier is empty
        if frontier.empty():
            print('Empty: No solution')
            return None

        # do not check results every single iteration, it is costly.
        if iteration_number % 10 == 0:
            goal_check = frontier.contains_state(target)

        # check if it is the goal
        if goal_check:
            # run through frontier nodes until you find your solution
            for node in frontier.frontier:
                if node.state == target:
                    # found it
                    movies, person_ids = [], []

                    while node.parent is not None:
                        person_ids.append(node.state)
                        movies.append(node.action)
                        node = node.parent

                    movies.reverse()
                    person_ids.reverse()
                    return list(zip(movies, person_ids))

        # remove node from frontier
        node = frontier.remove()

        current_state = node.state

        # update explored set, so we don't explore it once more
        explored_set.add(current_state)

        # nodes to include in the frontier - available options we can explore next
        neighbors = neighbors_for_person(current_state)
        
        # x[0] is the movie_id (action)
        # x[1] is the person_id (state)
        available_nodes = set(map(lambda x: Node(x[1], node, x[0]), neighbors))

        # include a state in the frontier if and only if: 
        # not already in the explored set AND not already in the frontier
        for each_node in available_nodes:
            node_state = each_node.state
            # check existence in set is O(1), so it is quite fast.
            if not node_state in explored_set:
                # .contains_state is O(N) within the frontier size. 
                # it has to run through all nodes in the frontier and check.
                # so we just want to perform it wisely.
                if not frontier.contains_state(node_state):
                    frontier.add(each_node)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
