import numpy as np
import random
import read_problem
import utils_distance
import utils_qlearning
import utils_aco
import utils_pco
import utils_generate_graph

problem_instance = read_problem.vrp_problem('problems/M-n200-k17')

def prepare_customer_data(problem_instance):
    customer_coords = problem_instance.instance.customers
    customer_demands = problem_instance.instance.demands[1:].reshape(-1,1)
    customer_coords_demands = np.hstack((customer_coords, customer_demands))

    customer_data = {}

    for i in range(len(customer_coords_demands)):
        customer_data[i+1] = tuple(customer_coords_demands[i])
    return customer_data

capacity = problem_instance.instance.capacity
demands = problem_instance.instance.demands
num_epochs = 1000
learning_rate = 0.1
discount_factor = 0.6
epsilon = 0.1
num_ants = 20
num_iterations = 100
pheromone_evaporation_rate = 0.25
pheromone_deposit_rate = 1
alpha = 1
num_particles = 10
c1 = 2  # Cognitive parameter
c2 = 2  # Social parameter
w = 0.5  # Inertia weight
beta = 2
Q = 100

customer_data = prepare_customer_data(problem_instance)
distances = utils_distance.calculate_distances(customer_data)

best_cost = []
best_route = []
for i in range(50):
    routes = utils_qlearning.q_learning(customer_data,capacity, epsilon, distances, learning_rate, discount_factor)
    aco_route = utils_aco.get_aco_optimized_path(customer_data, num_iterations, num_ants, routes, demands, pheromone_evaporation_rate, distances, Q, capacity)
    pso_route , pso_fitness= utils_pco.get_pco_optimized_route(customer_data, capacity, num_particles, num_iterations, c1, c2, w, demands, routes)
    aco_cost=utils_distance.calculate_cost(aco_route, distances)
    pso_cost=utils_distance.calculate_cost(pso_route, distances)
    if (aco_route[-1] and aco_route[-2]) == 0:
        aco_route = aco_route[:-1]
    if (pso_route[-1] and pso_route[-2]) == 0:
        pso_route = pso_route[:-1]
    best_cost.append(aco_cost if aco_cost<pso_cost else pso_cost)
    best_route.append(aco_route if aco_cost<pso_cost else pso_route)

mean_cost = (sum(best_cost)/len(best_cost))
print("Mean Cost :",mean_cost)

least_cost_idx = best_cost.index(min(best_cost))
print("Least Cost Obtained :",best_cost[least_cost_idx])
print("Best Route Obtained :",best_route[least_cost_idx])

utils_generate_graph.GenerateAndSaveGraph(best_route[least_cost_idx], problem_instance.instance.coordinates, problem_instance.name)

