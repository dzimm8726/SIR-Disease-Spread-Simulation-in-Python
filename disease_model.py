import random


def infect(infection_probability):
    '''
    Simulates the infection based on probability
    :param infection_probability: (float) Chance of infection (float between zero and one)
    :return:
    True or false based on if an infection occurs
    '''
    has_infection_occurred = random.uniform(0, 1)
    if has_infection_occurred < infection_probability:
        return True
    else:
        return False


def infect_test(num_times):
    '''
    Test the infect() function again and again to see the rate of the infection
    :param num_times: (int) Number of times to test infection
    :return:
    tuple: a count of infected and not infected cases (infected, uninfected)
    '''
    total_infected = 0
    total_uninfected = 0
    for trial in range(num_times):
        result = infect(.2)
        if result:
            total_infected += 1
        else:
            total_uninfected += 1
    return total_infected, total_uninfected


def recover(recovery_probability):
    '''
    Simulates recovery based on a probability.

    :param recovery_probability: (float): Chance of recovery (between 0 and 1)

    :return:
    bool: True or false based off if the person recovers

    '''
    has_recovery_occurred = random.uniform(0, 1)
    if has_recovery_occurred < recovery_probability:
        return True
    else:
        return False


def contact_indices(pop_size, source, contact_range) -> list:
    '''
    Finds the indices of people who come in contact with an infected person.

    :param pop_size: (int): Total population size
    :param source: (int): Index of infected person
    :param contact_range: (int): How many people nearby can be infected

    :return:
    list[int]: List of indices of people in contact range
    '''
    start = max(0, source - contact_range)
    end = min(pop_size - 1, source + contact_range)

    contacts = [i for i in range(start, end + 1) if i != source]

    return contacts


def apply_recoveries(population, recovery_probability):
    '''
    Applies recovery chance to all infected people in the population.
    :param population: (list): List of what people are ('S', 'I', or 'R')
    :param recovery_probability:(float): Chance of recovery

    :return:
    list: Updated population after recoveries

    '''
    for i in range(len(population)):
        if population[i] == "I":
            if recover(recovery_probability):
                population[i] = "R"
    return population


def contact(population, source, contact_range, infect_chance):
    '''
    Simulates contact between an infected person and nearby susceptible people.

    :param population: (list): List of peoples statuses
    :param source: Index of infected person
    :param contact_range: (int): How many people nearby can be infected
    :param infect_chance: (float): Chance of infection when contact occurs.

    '''
    contacts = contact_indices(len(population), source, contact_range)
    for person_index in contacts:
        if population[person_index] == 'S':
            if infect(infect_chance):
                population[person_index] = 'I'


def apply_contacts(population, contact_range, infect_chance):
    '''
    Applies contact simulation for all infected people in the population.

    :param population: (list): List of people's statuses
    :param contact_range:(int): How many people nearby can be infected
    :param infect_chance: (float): Chance of infection when contact occurs

    '''
    infected_indices = [i for i, status in enumerate(population) if status == 'I']
    for source in infected_indices:
        contact(population, source, contact_range, infect_chance)


def population_SIR_counts(population):
    """
    Counts how many people are in each SIR category
    :param population: (list): List of peoples statuses
    :return:
    dict: Counts of susceptible, infected, and recovered people
    """
    counts = {
        'susceptible': 0,
        'infected': 0,
        'recovered': 0
    }

    for status in population:
        if status == 'S':
            counts['susceptible'] += 1
        elif status == 'I':
            counts['infected'] += 1
        elif status == 'R':
            counts['recovered'] += 1

    return counts


def simulate_day(population, contact_range, infect_chance, recover_chance):
    '''
    Simulates one day of the disease spread.
    :param population: (list): List of peoples statuses
    :param contact_range: (int): How many people nearby can be infected
    :param infect_chance: (float): Chance of infection when contact occurs
    :param recover_chance: (float): Chance of recovery
    '''
    apply_recoveries(population, recover_chance)
    apply_contacts(population, contact_range, infect_chance)


def recovery_test(num_times):
    '''
    Tests the recovery function multiple times to see average recoveries.

    :param num_times: (int): Number of times to test recovery
    :return:
    float: Average number of recoveries
    '''
    result = []
    for _ in range(num_times):
        population = ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']
        apply_recoveries(population, .3)
        result.append(population.count('R'))
    return sum(result) / len(result)


def initialize_population(pop_size: int) -> list:
    '''
    Creates initial population with one infected person
    :param pop_size: (int): Total number of people
    :return:
    list: Population list with all 'S' (susceptible) except first person is 'I' (infected)
    '''
    population = ['S'] * pop_size
    population[0] = 'I'
    return population


def simulate_disease(pop_size: int, contact_range: int, infect_chance: float, recover_chance: float) -> list:
    '''
    Runs full disease simulation until no more infected people remain.
    :param pop_size: (int): Total number of people
    :param contact_range: (int): How many people nearby can be infected
    :param infect_chance: (float): Chance of infection when contact occurs
    :param recover_chance: Chance of recovery
    :return:
    list: Daily counts of SIR categories
    '''
    population = initialize_population(pop_size)
    counts = population_SIR_counts(population)
    all_counts = [counts]
    while counts['infected'] > 0:
        simulate_day(population, contact_range, infect_chance, recover_chance)
        counts = population_SIR_counts(population)
        all_counts.append(counts)
    return all_counts


def peak_infections(all_counts: list) -> int:
    '''
    Finds the highest number of infections during the simulation
    :param all_counts: (list): Daily counts of SIR categories
    :return:
    int: Maximum number of infections at any time
    '''
    max_infections = 0
    for day in all_counts:
        if day['infected'] > max_infections:
            max_infections = day['infected']
    return max_infections


def display_results(all_counts: list) -> None:
    '''
    Prints simulation results in a table format
    :param all_counts: (list): Daily counts of SIR categories
    '''
    num_days = len(all_counts)
    days, sus, inf, rec = 'Day', 'Susceptible', 'Infected', 'Recovered'
    print(f'{days:>12}{sus:>12}{inf:>12}{rec:>12}')
    for day in range(num_days):
        print(f'{str(day):>12}{all_counts[day]["susceptible"]:>12}{all_counts[day]["infected"]:>12}'
              f'{all_counts[day]["recovered"]:>12}')
    print(f'\nPeak Infections: {peak_infections(all_counts)}')


if __name__ == '__main__':
    counts = simulate_disease(100, 2, .2, .05)
    display_results(counts)