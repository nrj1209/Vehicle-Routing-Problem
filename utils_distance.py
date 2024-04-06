import numpy as np

def calculate_distances(customer_data):
    # Calculate distances between customers
    num_customers = len(customer_data.keys())
    distances = np.zeros((num_customers + 1, num_customers + 1))
    for i in range(1, num_customers + 1):
        for j in range(1, num_customers + 1):
            if i != j:
                distances[i][j] = np.sqrt((customer_data[i][0] - customer_data[j][0]) ** 2 +
                                        (customer_data[i][1] - customer_data[j][1]) ** 2)
    
    return distances

def calculate_cost(route, distance_matrix):
    cost = 0
    for i in range(len(route) - 1):
        start_node = route[i]
        end_node = route[i + 1]
        cost += distance_matrix[start_node][end_node]
    return cost