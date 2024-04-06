import matplotlib.pyplot as plt
from copy import deepcopy

def GenerateAndSaveGraph(vrp_path_indices,node_coordinates,problem_name):
    vrp_path_coordinates = []
    temp = []
    for i in vrp_path_indices:
        if(i==0 and temp!=[]):
            temp.append(node_coordinates[i])
            vrp_path_coordinates.append(deepcopy(temp))
            temp.clear()
            temp.append(node_coordinates[i])
        else:
            temp.append(node_coordinates[i])
            
    num_paths = len(vrp_path_coordinates)
    colors = [plt.cm.jet(i / float(num_paths)) for i in range(num_paths)] 

    fig, ax = plt.subplots(figsize=(10, 10))

    for i, vrp_path in enumerate(vrp_path_coordinates):
        color = colors[i]
        x, y = zip(*vrp_path)
        plt.plot(x, y, marker='o', color=color, label=f'Path {i + 1}')

    x_coordinates, y_coordinates = zip(*[point for path in vrp_path_coordinates for point in path])
    ax.set_xlim(min(x_coordinates) - 20, max(x_coordinates) + 20)
    ax.set_ylim(min(y_coordinates) - 20, max(y_coordinates) + 20)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")

    plt.legend()
    plt.savefig('solutions/'+problem_name+'.png')
    plt.show()
    