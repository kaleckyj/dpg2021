from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import math
import random

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

#processor 0 generates etalons and sends them to every other processor
if rank==0:
    etalons = []
    for n in range(size):
        etalon = (round(random.uniform(-5,5), 4), round(random.uniform(-5,5), 4))
        etalons.append(etalon)
    for i in range(0, size):
        comm.isend(etalons,dest=i,tag=11)

#each processor generates points which they assign to an etalon
req = comm.irecv(source=0,tag=11)
etalons = req.wait()

points = []
for n in range(100):
    x = random.uniform(-5,5)
    y = random.uniform(-5,5)

    #move the coords around the etalon
    rand_op = random.getrandbits(2)
    if rand_op == 0:
        point = (round(x + etalons[rank][0],4), round(y + etalons[rank][0],4))
    elif rand_op == 1:
        point = (round(x + etalons[rank][0],4), round(y - etalons[rank][0],4))
    elif rand_op == 2:
        point = (round(x - etalons[rank][0],4), round(y - etalons[rank][0],4))
    elif rand_op == 3:
        point = (round(x - etalons[rank][0],4), round(y + etalons[rank][0],4))
    points.append(point)

#at this point i want to gather all the points so i can plot them
unclassified = comm.gather(points, root=0)
if rank==0:
    print("please plot unclassified points")
    unclassified_points = [item for sublist in unclassified for item in sublist]
    #TO-DO plot me

#each processor recalculates the distances between each point and etalon
for i, point in enumerate(points):
    min_dist = 1000
    for n in range(len(etalons)):
        dist = math.sqrt((point[0]-etalons[n][0])**2+(point[1]-etalons[n][1])**2) #sqrt((xp-xc)^2(yp-yc)^2
        if dist < min_dist:
            points[i] = (point[0], point[1], n)
            min_dist = dist

#now i want to gather all classified points and plot them
classified = comm.gather(points, root=0)
if rank==0:
    print("please plot classified points and save the graph")
    classified_points = [item for sublist in classified for item in sublist]
    #TO-DO plot me
