from disease_model import population_SIR_counts, simulate_day


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
    :param recover_chance: (float): Chance of recovery
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
    counts = simulate_disease(1000, 2, .2, .05)
    display_results(counts)