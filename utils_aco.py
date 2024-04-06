import numpy as np
import random

def construct_solution(route, demands, capacity):
    ant_solution = [0]  # Start from the depot
    current_capacity = 0
    current_location = 0  # Depot
    visited = set()  # Track visited customers
    for customer in route[1:]:
        if customer == 0:
            ant_solution.append(customer)
            current_capacity = 0
            current_location = customer
        elif current_capacity + demands[customer] <= capacity and customer not in visited:
            ant_solution.append(customer)
            current_capacity += demands[customer]
            current_location = customer
            visited.add(customer)
        elif customer in visited:
            # Skip the customer if already visited
            continue
        else:
            # Return to depot if capacity exceeded
            ant_solution.append(0)
            ant_solution.append(customer)
            current_capacity = demands[customer]
            current_location = customer
            visited.add(customer)
    # Ensure all customers are visited exactly once
    unvisited_customers = set(demands.keys()) - visited
    for customer in unvisited_customers:
        if customer != 0:
            ant_solution.append(customer)
            ant_solution.append(0)
    ant_solution.append(0)  # Return to depot at the end
    return ant_solution

def update_pheromone(pheromone, solutions, pheromone_evaporation_rate, Q, distance_matrix):
    delta_pheromone = np.zeros_like(pheromone)
    for solution in solutions:
        for i in range(len(solution) - 1):
            start_node = solution[i]
            end_node = solution[i+1]
            delta_pheromone[start_node, end_node] += Q / distance_matrix[start_node, end_node]
    pheromone = (1 - pheromone_evaporation_rate) * pheromone + delta_pheromone
    return pheromone


def get_aco_optimized_path(customer_data, num_iterations, num_ants, routes, orig_demands, pheromone_evaporation_rate, distance_matrix, Q, capacity):
    demands = {}
    for i in range(len(orig_demands)):
        demands[i] = orig_demands[i]
    num_customers = len(customer_data.keys())
    # Initialize pheromone matrix
    pheromone = np.ones((num_customers + 1, num_customers + 1))
    # Main ACO loop
    for iteration in range(num_iterations):
        ant_solutions = []
        for ant in range(num_ants):
            # Choose a route for the ant
            route_index = random.randint(0, 1)
            ant_solution = construct_solution(routes[route_index], demands, capacity)
            ant_solutions.append(ant_solution)
        pheromone = update_pheromone(pheromone, ant_solutions, pheromone_evaporation_rate, Q, distance_matrix)

    # Select the best solution found so far as the final route
    # This can be based on the total distance or other criteria
    best_solution_index = np.argmax([sum(demands[node] for node in solution) for solution in ant_solutions])
    best_route = ant_solutions[best_solution_index]

    # print("Best Route:", best_route)
    return best_route


