import vrplib

class vrp_instance:
    def __init__(self,instance_path):
        self.__instance = vrplib.read_instance(instance_path+ ".vrp")
        self.name = self.__instance['name']
        self.dimension = self.__instance['dimension']
        self.capacity = self.__instance['capacity']
        self.coordinates = self.__instance['node_coord']
        self.customers = self.coordinates[1:]
        self.depot = self.coordinates[0]
        self.demands = self.__instance['demand']
        self.edge_weights = self.__instance['edge_weight']

class vrp_solution:
    def __init__(self,solution_path):
        self.__solution = vrplib.read_solution(solution_path+ ".sol")
        self.routes = self.__solution['routes']
        self.best_cost = self.__solution['cost']

class vrp_problem:
    def __init__(self,instance_name):
        self.name = instance_name
        self.instance = vrp_instance(self.name)
        self.solution = vrp_solution(self.name)
