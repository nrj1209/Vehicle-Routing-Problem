import numpy as np
import random

def q_learning(customer_data,capacity, epsilon, distances, learning_rate, discount_factor):
    num_customers = len(customer_data.keys())
    Q = np.zeros((num_customers + 1, num_customers + 1))  # Q-table
    all_routes = []

    for _ in range(10):  # Generate 10 different routes
        current_capacity = capacity
        current_location = 0  # Start at depot
        unvisited_customers = list(range(1, num_customers + 1))
        route = [0]

        while len(unvisited_customers) > 0:
            if random.uniform(0, 1) < epsilon:
                next_customer = random.choice(unvisited_customers)
            else:
                next_customer = np.argmax(Q[current_location])

            if next_customer not in unvisited_customers:
                next_customer = random.choice(unvisited_customers)

            next_location = next_customer
            demand = customer_data[next_location][2]
            if demand <= current_capacity:  # Check if vehicle can serve the demand
                current_capacity -= demand
            else:
                route.append(0)  # Return to depot if capacity is insufficient
                current_location = 0
                current_capacity = capacity
                continue

            route.append(next_location)
            current_location = next_location

            if next_customer in unvisited_customers:
                unvisited_customers.remove(next_customer)

            # Q-table update
            reward = -distances[current_location][next_location]
            Q[current_location][next_location] += learning_rate * (
                reward + discount_factor * np.max(Q[next_location]) - Q[current_location][next_location]
            )

        route.append(0)  # End at depot

        all_routes.append(route)

    return all_routes[-10:]