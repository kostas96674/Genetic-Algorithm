import random

graph = {

    1:{
        'neighbors' : [2,3,4,13,15,16],
        'score' : 0,
        },

    2: {
        'neighbors' : [1,3,5,8,9,16],
        'score' : 0,
        },

    3: {
        'neighbors' : [1,2,4,5,6],
        'score' : 0,
        },

    4: {
        'neighbors' : [1,3,6,13,15,16],
        'score' : 0,
        },

    5: {
        'neighbors' : [2,3,6,7,9,10],
        'score' : 0,
        },

    6: {
        'neighbors' : [3,4,5,7,11,13],
        'score' : 0,
        },

    7: {
        'neighbors' : [5,6,10,11],
        'score' : 0,
        },

    8: {
        'neighbors' : [2,9,14,16],
        'score' : 0,
        },

    9: {
        'neighbors' : [2,5,8,10,12,14],
        'score' : 0,
        },

    10:{
        'neighbors' : [5,7,9,11,12],
        'score' : 0,
        },

    11:{
        'neighbors' : [6,7,10,12,13],
        'score' : 0,
        },

    12:{
        'neighbors' : [9,10,11,13,14,15],
        'score' : 0,
        },

    13:{
        'neighbors' : [1,4,6,11,12,15,16],
        'score' : 0,
        },

    14:{
        'neighbors' : [2,8,9,12,15,16],
        'score' : 0,
        },

    15:{
        'neighbors' : [1,2,12,13,14,16],
        'score' : 0,
        },

    16:{
        'neighbors' : [1,2,15],
        'score' : 0,
        }
}

def create_population(population_size):
    characters = ["G", "B", "Y", "R"]
    strings = []
    for _ in range(population_size):
        string = ''.join(random.choice(characters) for _ in range(16))
        strings.append(string)
    return strings

def calculate_fitness(generated_strings,total_score):

    string_scores = []
    string_score = 0

    for colored_string in generated_strings:
        string_score = 0
        for colored_box, dic in graph.items():
            for neighbor in dic['neighbors']:
                graph[colored_box]['score'] = 0
        for colored_box, dic in graph.items():
            for neighbor in dic['neighbors']:
                if colored_string[neighbor-1] != colored_string[colored_box-1]:
                    graph[colored_box]['score'] += 1
            string_score += graph[colored_box]['score']
        total_score += string_score
        string_scores.append(string_score)
    return string_scores,total_score

def pick_range(string_scores):
    pick_range = []
    previous_score = string_scores[0]
    pick_range.append(previous_score)
    for i in range(100):
        if string_scores[i] != string_scores[0]:
            previous_score += string_scores[i]
            pick_range.append(previous_score)
    return pick_range

def pick_index(random_value, my_list):
    for i in range(len(my_list)):
        if random_value <= my_list[i]:
            return i
    return len(my_list) - 1

def parent_selection(percentage,pick_ranges,total_score):
    iterations = int((len(generated_strings)*percentage)/100)
    selected_parents = []
    for _ in range(iterations):
        random_value = random.randint(1, total_score)
        i = pick_index(random_value,pick_ranges)
        selected_parents.append(generated_strings[i])
    total_score = 0
    return selected_parents,total_score

def crossover_parents(parents):
    num_parents = len(parents)
    if num_parents % 2 != 0:
        last_parent = parents[-1]
        random_parent = random.choice(parents[:-1])
        pairs = [(parents[i], parents[i+1]) for i in range(0, num_parents-1, 2)]
        pairs.append((last_parent, random_parent))
    else:
        pairs = [(parents[i], parents[i+1]) for i in range(0, num_parents, 2)]

    new_strings = []
    for pair in pairs:
        parent1, parent2 = pair
        n = random.randint(1, len(parent1)-1)
        new_string1 = parent1[:n] + parent2[n:]
        new_string2 = parent2[:n] + parent1[n:]
        new_strings.append(new_string1)
        new_strings.append(new_string2)

    return new_strings

def mutate_parents(n):
    list_of_parents = create_population(n)
    return list_of_parents

def population_renewal(n):
    list_of_parents = create_population(n)
    return list_of_parents

def find_maximum_score(list_of_scores):
    max_score = max(list_of_scores)  # Find the maximum score in the list
    max_index = list_of_scores.index(max_score)  # Find the index of the maximum score
    return max_index

def biggest_integers_indexes(input_list,n):
    # Enumerate the input list to get both values and indexes
    enumerated_list = list(enumerate(input_list))

    # Sort the enumerated list based on the integer values in descending order
    sorted_list = sorted(enumerated_list, key=lambda x: x[1], reverse=True)

    # Extract the indexes of the n biggest integers
    indexes = [item[0] for item in sorted_list[:n]]

    return indexes

def extract_strings_by_indexes(string_list, indexes):
    new_list = []
    for index in indexes:
        if index < len(string_list):
            new_list.append(string_list[index])
    return new_list

def genetic_algorithm(generated_strings,total_score):
    i = 0
    string_scores,total_score = calculate_fitness(generated_strings,total_score)
    new_population = generated_strings
    if 87 in string_scores:
        index = string_scores.index(87)
        return generated_strings[index]
    else:
        while i < 100:
            if i != 0:
                string_scores,total_score = calculate_fitness(new_population,total_score)
                if 87 in string_scores:
                    index = string_scores.index(87)
                    return generated_strings[index]
            pick_ranges = pick_range(string_scores)
            selected_parents,total_score= parent_selection(60,pick_ranges,total_score)
            crossovered_parents = crossover_parents(selected_parents)
            mutated_parents = mutate_parents(20)
            new_parents = population_renewal(10)
            best_parents_indexes = biggest_integers_indexes(string_scores,10)
            best_parents = extract_strings_by_indexes(new_population, best_parents_indexes)

            new_population = crossovered_parents + mutated_parents + new_parents + best_parents

            i += 1
    index = find_maximum_score(string_scores)
    print(string_scores[index])
    return new_population[index]

generated_strings = create_population(100)

total_score = 0

best_coloring = genetic_algorithm(generated_strings,total_score)

print(best_coloring)
