import numpy as np

class Particle:
    def __init__(self, num_customers, capacity, distance_matrix, demand):
        self.num_customers = num_customers
        self.capacity = capacity
        self.distance_matrix = distance_matrix
        self.demand = demand
        self.position = np.zeros(num_customers + 2, dtype=int)  # Include two zeros for start and end
        self.velocity = np.zeros(num_customers + 2, dtype=int)  # Include two zeros for start and end
        self.best_position = None
        self.best_fitness = float('inf')
    
    def initialize(self):
        self.position[1:-1] = np.random.permutation(range(1, self.num_customers + 1))
        self.velocity[1:-1] = np.random.permutation(range(1, self.num_customers + 1))
        self.position[-1] = self.position[0]  # Set the last element to 0 for end
        self.velocity[-1] = self.velocity[0]  # Set the last element to 0 for end
        self.best_position = self.position.copy()
        self.best_fitness = self.fitness(self.position)
    
    def update_velocity(self, global_best_position, c1, c2, w):
        r1 = np.random.rand(self.num_customers + 2)
        r2 = np.random.rand(self.num_customers + 2)
        self.velocity = (w * self.velocity) + (c1 * r1 * (self.best_position - self.position)) + \
                        (c2 * r2 * (global_best_position - self.position))
    
    def update_position(self):
        self.position = np.argsort(self.position + self.velocity)
        self.position[-1] = self.position[0]  # Ensure the last element is 0 for end
    
    def fitness(self, position):
        fitness = 0
        current_capacity = self.capacity
        current_route = []
        
        for customer in position:
            if customer == 0:
                if current_route:
                    fitness += self.distance_matrix[current_route[-1], 0]
                current_route = []
                current_capacity = self.capacity
            else:
                demand = self.demand[customer]
                if demand <= current_capacity:
                    current_capacity -= demand
                else:
                    fitness = float('inf')  # Violation of capacity constraint
                    break
                current_route.append(customer)
        
        if current_route:
            fitness += self.distance_matrix[current_route[-1], 0]
        
        return fitness



def particle_swarm_optimization(num_customers, capacity, num_particles, num_iterations, c1, c2, w,
                                distance_matrix, demand, routes):
    particles = []
    global_best_position = None
    global_best_fitness = float('inf')
    
    # Initialize global_best_position with the position of the first particle
    # before entering the optimization loop
    first_particle = Particle(num_customers, capacity, distance_matrix, demand)
    first_particle.initialize()
    global_best_position = first_particle.best_position
    global_best_fitness = first_particle.best_fitness
    
    for _ in range(num_particles):
        particle = Particle(num_customers, capacity, distance_matrix, demand)
        particle.initialize()
        particles.append(particle)
        
    for _ in range(num_iterations):
        for particle in particles:
            particle.update_velocity(global_best_position, c1, c2, w)
            particle.update_position()
            
            current_fitness = particle.fitness(particle.position)
            if current_fitness < particle.best_fitness:
                particle.best_position = particle.position.copy()
                particle.best_fitness = current_fitness
            
            if current_fitness < global_best_fitness:
                global_best_position = particle.position.copy()
                global_best_fitness = current_fitness
                
    # Find the best route from the provided routes list
    best_route_fitness = float('inf')
    best_route = None
    for route in routes:
        route_fitness = first_particle.fitness(route)
        if route_fitness < best_route_fitness:
            best_route_fitness = route_fitness
            best_route = route
    
    return best_route, best_route_fitness


def get_pco_optimized_route(customer_data, capacity, num_particles, num_iterations, c1, c2, w, orig_demands, routes):
    demands = {}
    for i in range(len(orig_demands)):
        demands[i] = orig_demands[i]
    demands[i+1] = 0

    num_customers = len(customer_data.keys())
    distance_matrix = np.random.randint(1, 100, size=(num_customers + 2, num_customers + 2))  # Adjust size to (num_customers + 2, num_customers + 2)
    np.fill_diagonal(distance_matrix, 0)


    best_position, best_fitness = particle_swarm_optimization(num_customers, capacity, num_particles,
                                                            num_iterations, c1, c2, w,
                                                            distance_matrix, demands, routes)

    # print("Best route:",best_position)
    # print("Best fitness:", best_fitness)
    return best_position, best_fitness