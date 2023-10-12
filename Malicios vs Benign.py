import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import random
import time
import heapq
from prettytable import PrettyTable
import copy
import threading
import csv
from queue import Queue
import datetime
import numpy as np



class Vehicle:
    def __init__(self, ID, origin, destination, zone, time, current_node): #, time_reached_intersection, time_crossed, distance_away_from_intersection
        self.ID = ID

        if origin.lower() in ['east', 'west', 'north', 'south']:
            self.origin = origin
        elif destination.lower() in ['east', 'west', 'north', 'south']:
            self.destination = destination
        else:
            raise ValueError("Invalid origin.")
        self.destination = destination
        self.zone=zone  #distance away from the intersection
                        #D 40m away, C: 20m away, B: 20m away, A: 10m away
        self.time=time #current time on teh vehicle
        self.current_node = current_node
        # self.time_reached_intersection = time_reached_intersection
        # self.distance_away_from_intersection = distance_away_from_intersection
        # self.time_crossed = time_crossed

class Node:
    def __init__(self):
        self.vehicles = []
        self.time = 0
        self.presence = False

class Zone:
    def __init__(self, name):
        self.name = name
        self.vehicles = []

# Four arrays of request signal, each for each direction
north_queue = []
south_queue = []
east_queue = []
west_queue = []

# Arrays of confirmation signals, to show dequeue and queue to destination
# destination from north
N_E = []
N_S = []
N_W = []

# destination from south
S_E = []
S_N = []
S_W = []

# # destination from east
E_W = []
E_S = []
E_N = []

# destination from west
W_E = []
W_S = []
W_N = []

# Queues the REQUEST signal and assumes they all get CONFIRM signal from Int. BEFORE MOVING
NO=[]
NL=[]
NR=[]
NS=[]

SR=[]
SL=[]
SO=[]
SS=[]

EO=[]
EL=[]
ER=[]
ES=[]

WR=[]
WL=[]
WO=[]
WS=[]

   

Node1 = Node()
Node2 = Node()
Node3 = Node()
Node4 = Node()
Node5 = Node()
Node6 = Node()
Node7 = Node()
Node8 = Node()
Node9 = Node()
Node10 = Node()
Node11 = Node()
Node12 = Node()
Node13 = Node()
Node14 = Node()
Node15 = Node()
Node16 = Node()

ZoneA_SO= Node()
ZoneB_SO= Node()
ZoneC_SO= Node()
ZoneD_SO= Node()

ZoneA_SR= Node()
ZoneB_SR= Node()
ZoneC_SR= Node()
ZoneD_SR= Node()

ZoneA_SL= Node()
ZoneB_SL= Node()
ZoneC_SL= Node()
ZoneD_SL= Node()

ZoneA_NO= Node()
ZoneB_NO= Node()
ZoneC_NO= Node()
ZoneD_NO= Node()

ZoneA_NR= Node()
ZoneB_NR= Node()
ZoneC_NR= Node()
ZoneD_NR= Node()

ZoneA_NL= Node()
ZoneB_NL= Node()
ZoneC_NL= Node()
ZoneD_NL= Node()

ZoneA_WO= Node()
ZoneB_WO= Node()
ZoneC_WO= Node()
ZoneD_WO= Node()

ZoneA_WR= Node()
ZoneB_WR= Node()
ZoneC_WR= Node()
ZoneD_WR= Node()

ZoneA_WL= Node()
ZoneB_WL= Node()
ZoneC_WL= Node()
ZoneD_WL= Node()

ZoneA_EO= Node()
ZoneB_EO= Node()
ZoneC_EO= Node()
ZoneD_EO= Node()

ZoneA_ER= Node()
ZoneB_ER= Node()
ZoneC_ER= Node()
ZoneD_ER= Node()

ZoneA_EL= Node()
ZoneB_EL= Node()
ZoneC_EL= Node()
ZoneD_EL= Node()

ZoneA = Zone('A')
ZoneB = Zone('B')
ZoneC = Zone('C')
ZoneD = Zone('D')

Exited_north = Node()
Exited_south = Node()
Exited_east = Node()
Exited_west = Node()

all_queues = [SO, SR, SL, NO, NR, NL, EO, ER, EL, WO, WR, WL, SS, NS, WS, ES]  

queue_order_NSEW=[]
FROsorted_queue=[]
node_headway_seconds=1
storage_time=2
formatted_time=0

#plotting arrays for benign
Y=[]
x1=[]
x2=[]
x3=[]
x4=[]
x5=[]
x6=[]
x7=[]
x8=[]
x9=[]
x10=[]
x11=[]
x12=[]
x13=[]
x14=[]
xEm2=[]
xEm4=[]
X = [x1, x2, x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,xEm2,xEm4]
characters_after_x=[]
# Extract array names
array_names = [var_name for var_name, var_value in locals().items() if var_value in X]

def get_second_letter(name):
    # Create an array C containing x1 through x15
    C=[]
    C.append(name)

    # Extract array names and characters after 'x'
    array_names = [var_name for var_name, var_value in locals().items() if var_value in C]
    characters_after_x = [name.split('x')[1] for name in array_names]

    return characters_after_x
  # This will print ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']



import itertools
# Create a list of lists with 16 inner lists, each initialized with 8 zeros
# x_axis_time_list = [list(itertools.repeat(0, 8)) for i in range(16)]   #16col x 8 rows
# # Convert the list of lists to a NumPy array
# # x_axis_time = np.array(x_axis_time_list)

# # y axis IDs
# y_axis_ID_list = (list(itertools.repeat(0,1)) for i in range(16)) #16 columns
# Convert the list of lists to a NumPy array
# y_axis_ID = np.array(y_axis_ID_list)

# print(x_axis_time.shape) 16x8
# print(y_axis_ID.shape) 16x1

def generate_fixed_imposter_ID():
    vehID1=Vehicle(1, 'north', 'east')
    vehID2=Vehicle('Em1', 'east', 'south')
    vehID3=Vehicle(2, 'north', 'west')
    vehID4=Vehicle(3, 'north', 'west')
    vehID5=Vehicle(4, 'west', 'north')
    vehID6=Vehicle('Em5', 'west', 'east')
    vehID7=Vehicle(6, 'west', 'south')
    vehID8=Vehicle(7, 'south', 'west')
    vehID9=Vehicle('RealEm2', 'north', 'west')
    vehID10=Vehicle(8, 'south', 'east')
    vehID11=Vehicle(9, 'south', 'north')
    vehID12=Vehicle('Em3', 'west', 'north')
    vehID13=Vehicle(10, 'east', 'west')
    vehID14=Vehicle(11, 'east', 'west')
    vehID15=Vehicle(12, 'east', 'north')
    vehID20=Vehicle('RealEm4', 'south', 'west')
    
# Queues the REQUEST signal and assumes they all get CONFIRM signal from Int. Manager 
def queue_vehicle_request_from_origin(vehicle, origin):
    if vehicle.origin == 'north':
        north_queue.append(vehicle)
    elif vehicle.origin == 'south':
        south_queue.append(vehicle)
    elif vehicle.origin == 'east':
        east_queue.append(vehicle)
    elif vehicle.origin == 'west':
        west_queue.append(vehicle)

def generate_fixed_ID(): # Em2 and 4 are the only real EV
    global queue_order_NSEW, x_axis_ID, y_axis_time

   
    current_timestamp = datetime.datetime.now().strftime("%I:%M:%S %p")

    vehID1=Vehicle(1, 'north', 'east', 'A', current_timestamp,'' )
    vehID2=Vehicle(14, 'east', 'south', 'B', current_timestamp, '')
    vehID3=Vehicle(2, 'north', 'west', 'A', current_timestamp,'')
    vehID4=Vehicle(3, 'north', 'west', 'B', current_timestamp,'')
    vehID5=Vehicle(4, 'west', 'north', 'A', current_timestamp,'')
    vehID6=Vehicle(5, 'west', 'east', 'A', current_timestamp,'')
    vehID7=Vehicle(6, 'west', 'south', 'A', current_timestamp,'')
    vehID8=Vehicle(7, 'south', 'west', 'A', current_timestamp,'')
    vehIDEm2=Vehicle('emergency2', 'north', 'west', 'B', current_timestamp,'')
    vehID10=Vehicle(8, 'south', 'east', 'A', current_timestamp,'')
    vehID11=Vehicle(9, 'south', 'north', 'B', current_timestamp,'')
    vehID12=Vehicle(13, 'west', 'north', 'B', current_timestamp,'')
    vehID13=Vehicle(10, 'east', 'west', 'B', current_timestamp,'')
    vehID14=Vehicle(11, 'east', 'west', 'A', current_timestamp,'')
    vehID15=Vehicle(12, 'east', 'north', 'B', current_timestamp,'')
    vehIDEm4=Vehicle('emergency4', 'south', 'west', 'B', current_timestamp,'')

    queue_order_NSEW = [
    vehID1,
    vehID2,
    vehID3,
    vehID4,
    vehID5,
    vehID6,
    vehID7,
    vehID8,
    vehIDEm2,
    vehID10,
    vehID11,
    vehID12,
    vehID13,
    vehID14,
    vehID15,
    vehIDEm4]

    

    for i in queue_order_NSEW:
        Y.append(i.ID) #size

    x1.append(vehID1.time)
    x2.append(vehID2.time)
    x3.append(vehID3.time)
    x4.append(vehID4.time)
    x5.append(vehID5.time)
    x6.append(vehID6.time)
    x7.append(vehID7.time)
    x8.append(vehID8.time)
    xEm2.append(vehIDEm2.time)
    x10.append(vehID10.time)
    x11.append(vehID11.time)
    x12.append(vehID12.time)
    x13.append(vehID13.time)
    x14.append(vehID14.time)
    xEm4.append(vehIDEm4.time)
    

        

def save_time(veh):
    vehicle='x'+ str(veh.ID)
    if vehicle=='x1':
        x1.append(veh.time) 
    elif vehicle == 'x2':
        x2.append(veh.time)
    elif vehicle == 'x3':
        x3.append(veh.time)
    elif vehicle == 'x4':
        x4.append(veh.time)
    elif vehicle == 'x5':
        x5.append(veh.time)
    elif vehicle == 'x6':
        x6.append(veh.time)
    elif vehicle == 'x7':
        x7.append(veh.time)
    elif vehicle == 'x8':
        x8.append(veh.time)
    elif vehicle == 'emergency2':
        xEm2.append(veh.time)
    elif vehicle == 'x10':
        x10.append(veh.time)
    elif vehicle == 'x11':
        x11.append(veh.time)
    elif vehicle == 'x12':
        x12.append(veh.time)
    elif vehicle == 'x13':
        x13.append(veh.time)
    elif vehicle == 'x14':
        x14.append(veh.time)
    elif vehicle == 'emergency4':
        xEm4.append(veh.time)



def get_queue_name(queue_value):
    # Create a dictionary to map the queue names to their corresponding values
    queues_dict = {
        'SO': SO,
        'SR': SR,
        'SL': SL,
        'NO': NO,
        'NR': NR,
        'NL': NL,
        'EO': EO,
        'ER': ER,
        'EL': EL,
        'WO': WO,
        'WR': WR,
        'WL': WL,

        'SS': SS,
        'NS': NS,
        'ES': ES,
        'WS': WS,
    }

    for name, value in queues_dict.items():
        if value is queue_value:
            return name
    return None
    

# takes in vehicle to be appended on to a input queue, returns a formatted time
def accumulate_queue(queue, vehicle):
    current_timestamp = time.time()

    #if current_timestamp - current_time >= delay:
    queue.append(vehicle)
    queue_name= get_queue_name(queue)
    
    formatted_time = time.strftime("%I:%M %p", time.localtime(current_timestamp))
    #time.sleep(2)
    #print(vehicle.ID, " requests ", queue_name, " at ", formatted_time)
    
    return formatted_time
    #else:
       #return current_time

# # For a vehicle input, it appends to specific lane arrays [So, NO, ....]
# # And sleeps two seconds after each append
# def get_waiting_queue(vehicle):
#     global SR, SL, SO, NO, NR, NL, EO, ER, EL, WO, WR, WL

#     current_time = 0  # Initialize the current time
#     delay = 2  # 2 seconds delay

#     # for i in range(len(queue)):
#     # vehicle = queue[i]
#     # origin_prefix = vehicle.origin[0].upper()
#     # destination_prefix = vehicle.destination[0].upper()
#     time_crossing=2

#     origin_prefix = vehicle.origin[0].upper()
#     destination_prefix = vehicle.destination[0].upper()
#     # queue_name = get_queue_name(queue)
#     # formatted_time = time.strftime("%I:%M %p", time.localtime(time.time()))



#     if origin_prefix == 'S':
#         if destination_prefix == 'N':
#             current_time = accumulate_queue(SO, vehicle)
#             time.sleep(time_crossing)
#             # print(vehicle.ID, " requests ", get_queue_name(SO), " at ", current_time, " to distance zone ", "assigned_distance")

#         elif destination_prefix == 'E':
            
#             current_time = accumulate_queue(SR, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'W':
            
#             current_time = accumulate_queue(SL, vehicle)
#             time.sleep(time_crossing)
#     elif origin_prefix == 'N':
#         if destination_prefix == 'S':
            
#             current_time = accumulate_queue(NO, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'E':
            
#             current_time = accumulate_queue(NL, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'W':
            
#             current_time = accumulate_queue(NR, vehicle)
#             time.sleep(time_crossing)
#     elif origin_prefix == 'E':
#         if destination_prefix == 'N':
            
#             current_time = accumulate_queue(ER, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'S':
           
#             current_time = accumulate_queue(EL, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'W':
            
#             current_time = accumulate_queue(EO, vehicle)
#             time.sleep(time_crossing)
#     elif origin_prefix == 'W':
#         if destination_prefix == 'N':
           
#             current_time = accumulate_queue(WL, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'S':
            
#             current_time = accumulate_queue(WR, vehicle)
#             time.sleep(time_crossing)
#         elif destination_prefix == 'E':
           
#             current_time = accumulate_queue(WO, vehicle)
#             time.sleep(time_crossing)

# attempt (failed) at storage movement and time
def waiting_area():
    global SR, SL, SO, NO, NR, NL, EO, ER, EL, WO, WR, WL
    distance_zone = ['A', 'B', 'C', 'D']
    generate_fixed_ID()

    for vehicle in queue_order_NSEW:
        get_waiting_queue(vehicle)

    # Create a list of tuples to associate each queue with an assigned distance zone
    queue_distance_tuples = [(SR, None), (SL, None), (SO, None), (NO, None), (NR, None), (NL, None), (ER, None), (EL, None), (WO, None), (WR, None), (WL, None)]

    # Assign distance zones to the tuples in a cyclic manner
    for i in range(len(queue_distance_tuples)):
        queue_distance_tuples[i] = (queue_distance_tuples[i][0], distance_zone[i % len(distance_zone)])

    # Iterate through each queue and print the assigned distance zone for each vehicle
    for queue, assigned_distance in queue_distance_tuples:
        for vehicle in queue:
            origin_prefix = vehicle.origin[0].upper()
            destination_prefix = vehicle.destination[0].upper()
            queue_name = get_queue_name(queue)
            formatted_time = time.strftime("%I:%M %p", time.localtime(time.time()))
            print(vehicle.ID, " requests ", queue_name, " at ", formatted_time, " to distance zone ", assigned_distance)

            # Simulate a 2-second delay before moving to the next zone
            time.sleep(2)

            # Move the vehicle to the next zone (A -> B -> C -> D)
            current_zone_index = distance_zone.index(assigned_distance)
            next_zone_index = (current_zone_index + 1) % len(distance_zone)
            assigned_distance = distance_zone[next_zone_index]

            # Update the assigned distance for the vehicle
            print(vehicle.ID, " moves to distance zone ", assigned_distance)

print("################### STORAGE ZONE ##########################")
# Call fn to generate fixed vehicles (not random)
generate_fixed_ID()

# fig, ax = plt.subplots()

# def plot_time_ID():
#     global x_axis_ID, y_axis_time, ax

#     ax.clear()
#     ax.plot(x_axis_ID, y_axis_time, marker='o', linestyle='-')
#     ax.set_xlabel('Vehicle ID')
#     ax.set_ylabel('Time')
#     ax.set_title('Vehicle Time vs. ID')

# # 'interval' is the time delay between updates in milliseconds
# interval = 1  # Adjust as needed
# ani = FuncAnimation(fig, plot_time_ID, frames=None, interval=interval)
#plt.show()

#PRE MOVEMENT
# For a vehicle input, it appends to specific lane arrays [So, NO, ....] (No time involved)
def accumulate_to_lanes(vehicle):
    global SR, SL, SO, NO, NR, NL, EO, ER, EL, WO, WR, WL
    global y_axis_time
    current_time = 0  # Initialize the current time
    delay = 2  # 2 seconds delay
    time_crossing = 2  # Time taken to cross the intersection

    origin_prefix = vehicle.origin[0].upper()
    destination_prefix = vehicle.destination[0].upper()

    if origin_prefix == 'S':
        if destination_prefix == 'N':
            queue = SO
        elif destination_prefix == 'E':
            queue = SR
        elif destination_prefix == 'W':
            queue = SL
    elif origin_prefix == 'N':
        if destination_prefix == 'S':
            queue = NO
        elif destination_prefix == 'E':
            queue = NL
        elif destination_prefix == 'W':
            queue = NR
    elif origin_prefix == 'E':
        if destination_prefix == 'N':
            queue = ER
        elif destination_prefix == 'S':
            queue = EL
        elif destination_prefix == 'W':
            queue = EO
    elif origin_prefix == 'W':
        if destination_prefix == 'N':
            queue = WL
        elif destination_prefix == 'S':
            queue = WR
        elif destination_prefix == 'E':
            queue = WO

    #current_timestamp = time.time()
    queue.append(vehicle)
    # queue_name = get_queue_name(queue)
    # formatted_time = time.strftime("%I:%M %p", time.localtime(current_timestamp))
    
    # time.sleep(time_crossing)
#PRE MOVEMENT
# Call above function to all the available vehicles in this code
for veh in queue_order_NSEW:
    accumulate_to_lanes(veh)


#STORAGE ZONE MOVEMENT & TIME STARTS
#For each lane {SO, NO..}, append it a zone class (A, B, C  or D). to show distance away from intersection
#CONTAINS PRINT(ID, ZONE, TIME)
# A is 10m away, B is 20m away, C is 30m away.... (D->C->B->A)
def accumulate_to_zone(lane):
    global y_axis_time
    for vehicle in lane:
        for zone in [ZoneD, ZoneC, ZoneB, ZoneA]:
            if vehicle.zone == zone.name:
                #current_queue = zone.vehicles
                zone.vehicles.append(vehicle)
                
                current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
                vehicle.time = current_time
                
                
                
                #zone.time = current_time
                #print(f"\nVehicle {vehicle.ID} entered {zone.name} at time {vehicle.time}")
               

                break
        #time.sleep(storage_time) #wait happens when moving from one zone to another, not now

#print(x2)
# Veh move from zone classes D to C to B to A, based on the initial position of vehicle veh.zone
#CONTAINS PRINT
def storage_lane_movement(lane):
    for veh in lane:
        accumulate_to_zone(lane)
        if veh.zone=='D' and veh in ZoneD.vehicles:
            ZoneD.vehicles.remove(veh)
            
            time.sleep(2)
            ZoneC.vehicles.append(veh)
            veh.zone='C'
            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")
            

            ZoneC.vehicles.remove(veh)
            time.sleep(2)
            ZoneB.vehicles.append(veh)
            veh.zone='B'
            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")

            ZoneB.vehicles.remove(veh)
            time.sleep(2)
            ZoneA.vehicles.append(veh)
            veh.zone='A'
            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")

            # time.sleep(2)
            # ZoneA.vehicles.remove(veh)

        elif veh.zone=='C' and veh in ZoneC.vehicles:
            ZoneC.vehicles.remove(veh)
            time.sleep(2)
            ZoneB.vehicles.append(veh)
            veh.zone='B'

            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")
            
            ZoneB.vehicles.remove(veh)
            time.sleep(2)
            ZoneA.vehicles.append(veh)
            veh.zone='A'

            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")

            # ZoneA.vehicles.remove(veh)
            # time.sleep(2)
            
        elif veh.zone=='B' and veh in ZoneB.vehicles:
            ZoneB.vehicles.remove(veh)
            time.sleep(2)
            ZoneA.vehicles.append(veh)
            veh.zone='A'
            

            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")


        elif veh.zone=='A' and veh in ZoneA.vehicles:
            ZoneA.vehicles.remove(veh)
            time.sleep(2)
            veh.zone='A'
            
            veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
            save_time(veh)
            print(f"Vehicle {veh.ID} entered {veh.zone} at time {veh.time}")

            # ZoneA.vehicles.remove(veh)
            # time.sleep(2)

#print("@@@@@@@@@@@@@@@@@", y_axis_time)              
# make threads to run the lane movement concurrently

all_queues = [SO, SR, SL, NO, NR, NL, EO, ER, EL, WO, WR, WL, SS, NS, WS, ES] 

all_storage_threads = []

# all vehicles in lanes move concurrently (vehicles remain in SO, NR.. lanes), bu move between zone classes
for i in all_queues:
    thread_storage_movement= threading.Thread(target=storage_lane_movement, args=(i,))
    all_storage_threads.append(thread_storage_movement)
    thread_storage_movement.start()

# waits for all the threads to join 
for thread in all_storage_threads:
    thread.join()

print(x13)
# After all the vehicles has passed thorugh the waiting area and waited for its turn, passes through conflict zone

print("################### CONFLICT AREA ##########################")

#2 Clear the vehicles in front
def remove_veh_in_front(incoming):
    # Create a dictionary to map the second letter of array to the adjacent queue identifier
  #........
    for vehicle in incoming:
        if str(vehicle.ID).startswith('emergency'):
            emergency_vehicle = vehicle
            break
    else:
        return  # No emergency vehicle found in incoming queue

    # Move vehicles before the emergency vehicle to an adjacent queue
    emergency_vehicle_index = incoming.index(emergency_vehicle)
    # New queue of vehicles before the index of the emergency vehicle, [::-1] makes sure of reversing it ensuring that the vehicles are moved in the order they were originally queued.
    vehicles_to_move = incoming[:emergency_vehicle_index][::-1]  # Reverse to maintain the order
    
    # for i in vehicles_to_move:
    #     print("Vehicle in front of EV", i.ID)
    

    origin_queue_name = get_queue_name(incoming)  # Get the original queue name from the incoming input
    #print("################", origin_queue_name)
    #adjacent_queue_id = origin_queue_name[0] + adjacent_yielding_queue_map[origin_queue_name[1]]
    #adjacent_queue = next(q for q in all_queues if get_queue_name(q) == adjacent_queue_id)
    #print("############", adjacent_queue)
    #veh_togoback = adjacent_queue[:emergency_vehicle_index]

    # Move vehicles before the emergency vehicle to an adjacent queue
    #while incoming[0] != emergency_vehicle:
    for vehicle in vehicles_to_move:
        # if emergency_vehicle in vehicles_to_move:
        #     print("##########################Emergency vehicle is in veh_to_goback")
        vehicle = incoming.pop(0)
        #adjacent_queue.append(vehicle)
        #print("#############", adjacent_queue)
        
        print(f"\n\tYIELDing to {emergency_vehicle.ID}: Vehicle {vehicle.ID} moved from {origin_queue_name} at ", datetime.datetime.now().strftime("%I:%M:%S %p"))
        #print(f"\nEV MOVE: Moved Vehicle ID {vehicle.ID} from {origin_queue_name} to {get_queue_name(adjacent_queue)}")
        # Check if the emergency vehicle is in the list veh_to_goback
        #moved_vehicles.append(vehicle)
        queue_vehicle_request_from_origin(vehicle, vehicle.origin)

        time.sleep(1)
   
   ########## Refer FreeIM code to see code for vehicles to go back to the waiting queue

# CONFLICT ZONE MOVEMENT
def define_Nodes(incoming):
    global Node1, Node2, Node3, Node4, Node5, Node6, Node7, Node8, Node9, Node10, Node11, Node12, Node13, Node14, Node15, Node16, Exited_north, Exited_south, Exited_east, Exited_west
    count=0
    
    # Check if there's an emergency vehicle
    #convert IDs to string to identify 'emergency' veh
    has_emergency_vehicle = any(str(vehicle.ID).startswith('emergency') for vehicle in incoming)

    # If there's an emergency vehicle, handle it first
    if has_emergency_vehicle:
        #handle_emergency_vehicle(incoming)
        remove_veh_in_front(incoming)
        #time.sleep(node_headway_seconds)


    for i in range(len(incoming)):
        
        veh = incoming[0]  # starting from the first vehicle and onwards
        # print(i,"\n")
        # print(incoming,"\n")
        # print(veh,"\n")
        
        if veh.origin == 'south':
            if veh.destination == 'north':
                while not (Node1.presence or Node2.presence or Node3.presence or Node4.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node1.vehicles.append(veh.ID)
                        Node1.presence = True
                        Node1.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        veh.current_node = 'Node1'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node1 at time {veh.time}")
                        
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        Node1.vehicles.pop(0)
                        Node1.presence = False
                        Node1.time = 0
                        Node2.vehicles.append(veh.ID)
                        Node2.presence = True
                        Node2.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node2 at time {Node2.time}")
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        veh.current_node = 'Node2'
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node2.vehicles.pop(0)
                        Node2.presence = False
                        Node2.time = 0
                        Node3.vehicles.append(veh.ID)
                        Node3.presence = True
                        Node3.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node3 at time {Node3.time}")
                        veh.current_node = 'Node3'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        

                        Node3.vehicles.pop(0)
                        Node3.presence = False
                        Node3.time = 0
                        Node4.vehicles.append(veh.ID)
                        Node4.presence = True
                        Node4.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node4 at time {Node4.time}")
                        veh.current_node = 'Node4'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        

                        Node4.vehicles.pop(0)
                        Node4.presence = False
                        Node4.time = 0
                        Exited_north.vehicles.append(veh.ID)
                        Exited_north.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to north at time {Exited_north.time}")
                        veh.current_node = 'Exited_north'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break

            if veh.destination == 'west':
                while not (Node6.presence or Node8.presence or Node11.presence or Node10.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node6.vehicles.append(veh.ID)
                        Node6.presence = True
                        Node6.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node6 at time {Node6.time}")
                        veh.current_node = 'Node6'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node6.vehicles.pop(0)
                        Node6.presence = False
                        Node6.time = 0
                        Node8.vehicles.append(veh.ID)
                        Node8.presence = True
                        Node8.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node8 at time {Node8.time}")
                        veh.current_node = 'Node8'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node8.vehicles.pop(0)
                        Node8.presence = False
                        Node8.time = 0
                        Node11.vehicles.append(veh.ID)
                        Node11.presence = True
                        Node11.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node11 at time {Node11.time}")
                        veh.current_node = 'Node11'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node11.vehicles.pop(0)
                        Node11.presence = False
                        Node11.time = 0
                        Node10.vehicles.append(veh.ID)
                        Node10.presence = True
                        Node10.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node10 at time {Node10.time}")
                        veh.current_node = 'Node10'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node10.vehicles.pop(0)
                        Node10.presence = False
                        Node10.time = 0
                        Exited_west.vehicles.append(veh.ID)
                        Exited_west.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to west at time {Exited_west.time}")
                        veh.current_node = 'Exited_west'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break

            if veh.destination == 'east':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_east.vehicles.append(veh.ID)
                    Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (righ turn) east at time {Exited_east.time}")
                    veh.current_node = 'Right_Exited_east'
                    veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                    time.sleep(node_headway_seconds)
                    save_time(veh)
                    break

        if veh.origin == 'north':
            print(veh.ID)
            if veh.destination == 'east':
                while not (Node16.presence or Node15.presence or Node3.presence or Node5.presence):
                    # if not incoming:
                    #     break
                    print(count)
                    if incoming[0].ID == veh.ID:
                        print(veh.ID, " in east")
                        incoming.pop(0)
                        Node16.vehicles.append(veh)
                        Node16.presence = True
                        Node16.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node16 at time {Node16.time}")
                        veh.current_node = 'Node16'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node16.vehicles.pop(0)
                        Node16.presence = False
                        Node16.time = 0
                        Node15.vehicles.append(veh)
                        Node15.presence = True
                        Node15.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node15 at time {Node15.time}")
                        veh.current_node = 'Node15'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node15.vehicles.pop(0)
                        Node15.presence = False
                        Node15.time = 0
                        Node3.vehicles.append(veh)
                        Node3.presence = True
                        Node3.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node3 at time {Node3.time}")
                        veh.current_node = 'Node3'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node3.vehicles.pop(0)
                        Node3.presence = False
                        Node3.time = 0
                        Node5.vehicles.append(veh)
                        Node5.presence = True
                        Node5.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node5 at time {Node5.time}")
                        veh.current_node = 'Node5'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node5.vehicles.pop(0)
                        Node5.presence = False
                        Node5.time = 0
                        Exited_east.vehicles.append(veh)
                        Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to east at time {Exited_east.time}")
                        veh.current_node = 'Existed East'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break
                        #Node16.presence, Node15.presence, Node3.presence, Node5.presence = False, False, False, False
                        # count+=1
                        # if count==len(incoming):
                        #     break
                        #i+=1
            if veh.destination == 'south':
                while not (Node13.presence or Node12.presence or Node11.presence or Node9.presence):
                    # if not incoming:
                    #     break
                    

                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node13.vehicles.append(veh)
                        Node13.presence = True
                        Node13.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node13 at time {Node13.time}")
                        veh.current_node = 'Node13'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node13.vehicles.pop(0)
                        Node13.presence = False
                        Node13.time = 0
                        Node12.vehicles.append(veh)
                        Node12.presence = True
                        Node12.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node12 at time {Node12.time}")
                        veh.current_node = 'Node12'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node12.vehicles.pop(0)
                        Node12.presence = False
                        Node12.time = 0
                        Node11.vehicles.append(veh)
                        Node11.presence = True
                        Node11.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node11 at time {Node11.time}")
                        veh.current_node = 'Node11'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node11.vehicles.pop(0)
                        Node11.presence = False
                        Node11.time = 0
                        Node9.vehicles.append(veh)
                        Node9.presence = True
                        Node9.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node9 at time {Node9.time}")
                        veh.current_node = 'Node9'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node9.vehicles.pop(0)
                        Node9.presence = False
                        Node9.time = 0
                        Exited_south.vehicles.append(veh)
                        Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to south at time {Exited_south.time}")
                        veh.current_node = 'Exited_south'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break
                        # count+=1
                        # if count==len(incoming):
                        #     break
                    
            if veh.destination == 'west':
                # if not incoming:
                #     break
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_east.vehicles.append(veh)
                    Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (right turn) east at time {Exited_east.time}")
                    veh.current_node = 'Existed_east'
                    veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                    time.sleep(node_headway_seconds)
                    save_time(veh)
                    break
                # count+=1
                # if count==len(incoming):
                #     break

        if veh.origin == 'east':
            if veh.destination == 'south':
                while not (Node5.presence or Node2.presence or Node7.presence or Node6.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node5.vehicles.append(veh.ID)
                        Node5.presence = True
                        Node5.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node5 at time {Node5.time}")
                        veh.current_node = 'Node5'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node5.vehicles.pop(0)
                        Node5.presence = False
                        Node5.time = 0
                        Node2.vehicles.append(veh.ID)
                        Node2.presence = True
                        Node2.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node2 at time {Node2.time}")
                        veh.current_node = 'Node2'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node2.vehicles.pop(0)
                        Node2.presence = False
                        Node2.time = 0
                        Node7.vehicles.append(veh.ID)
                        Node7.presence = True
                        Node7.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node7 at time {Node7.time}")
                        veh.current_node = 'Node7'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node7.vehicles.pop(0)
                        Node7.presence = False
                        Node7.time = 0
                        Node6.vehicles.append(veh.ID)
                        Node6.presence = True
                        Node6.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node6 at time {Node6.time}")
                        veh.current_node = 'Node6'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node6.vehicles.pop(0)
                        Node6.presence = False
                        Node6.time = 0
                        Exited_south.vehicles.append(veh.ID)
                        Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to south at time {Exited_south.time}")
                        time.sleep(node_headway_seconds)
                        veh.current_node = 'Exited_south'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        save_time(veh)
                        break

            if veh.destination == 'west':
                while not (Node4.presence or Node15.presence or Node14.presence or Node13.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node4.vehicles.append(veh.ID)
                        Node4.presence = True
                        Node4.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node4 at time {Node4.time}")
                        veh.current_node = 'Node4'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node4.vehicles.pop(0)
                        Node4.presence = False
                        Node4.time = 0
                        Node15.vehicles.append(veh.ID)
                        Node15.presence = True
                        Node15.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node15 at time {Node15.time}")
                        veh.current_node = 'Node15'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node15.vehicles.pop(0)
                        Node15.presence = False
                        Node15.time = 0
                        Node14.vehicles.append(veh.ID)
                        Node14.presence = True
                        Node14.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node14 at time {Node14.time}")
                        veh.current_node = 'Node14'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node14.vehicles.pop(0)
                        Node14.presence = False
                        Node14.time = 0
                        Node13.vehicles.append(veh.ID)
                        Node13.presence = True
                        Node13.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node13 at time {Node13.time}")
                        veh.current_node = 'Node13'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node13.vehicles.pop(0)
                        Node13.presence = False
                        Node13.time = 0
                        Exited_west.vehicles.append(veh.ID)
                        Exited_west.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to west at time {Exited_west.time}")
                        veh.current_node = 'Exited_west'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break

            if veh.destination == 'north':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_south.vehicles.append(veh.ID)
                    Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (right turm) south at time {Exited_south.time}")
                    veh.current_node = 'Right_Exited_South'
                    veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                    time.sleep(node_headway_seconds)
                    save_time(veh)
                    break

        if veh.origin == 'west':
            if veh.destination == 'east':
                while not (Node10.presence or Node12.presence or Node14.presence or Node16.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node10.vehicles.append(veh.ID)
                        Node10.presence = True
                        Node10.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node10 at time {Node10.time}")
                        veh.current_node = 'Node10'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node10.vehicles.pop(0)
                        Node10.presence = False
                        Node10.time = 0
                        Node12.vehicles.append(veh.ID)
                        Node12.presence = True
                        Node12.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node12 at time {Node12.time}")
                        veh.current_node = 'Node12'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node12.vehicles.pop(0)
                        Node12.presence = False
                        Node12.time = 0
                        Node14.vehicles.append(veh.ID)
                        Node14.presence = True
                        Node14.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node14 at time {Node14.time}")
                        veh.current_node = 'Node14'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node14.vehicles.pop(0)
                        Node14.presence = False
                        Node14.time = 0
                        Node16.vehicles.append(veh.ID)
                        Node16.presence = True
                        Node16.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node16 at time {Node16.time}")
                        veh.current_node = 'Node16'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node16.vehicles.pop(0)
                        Node16.presence = False
                        Node16.time = 0
                        Exited_north.vehicles.append(veh.ID)
                        Exited_north.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to north at time {Exited_north.time}")
                        veh.current_node = 'Exited_north'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break

            if veh.destination == 'east':
                while not (Node9.presence or Node8.presence or Node7.presence or Node1.presence):
                    if incoming[0].ID == veh.ID:
                        incoming.pop(0)
                        Node9.vehicles.append(veh.ID)
                        Node9.presence = True
                        Node9.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node9 at time {Node9.time}")
                        veh.current_node = 'Node9'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node9.vehicles.pop(0)
                        Node9.presence = False
                        Node9.time = 0
                        Node8.vehicles.append(veh.ID)
                        Node8.presence = True
                        Node8.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node8 at time {Node8.time}")
                        veh.current_node = 'Node8'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node8.vehicles.pop(0)
                        Node8.presence = False
                        Node8.time = 0
                        Node7.vehicles.append(veh.ID)
                        Node7.presence = True
                        Node7.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node7 at time {Node7.time}")
                        veh.current_node = 'Node7'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node7.vehicles.pop(0)
                        Node7.presence = False
                        Node7.time = 0
                        Node1.vehicles.append(veh.ID)
                        Node1.presence = True
                        Node1.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) entered Node1 at time {Node1.time}")
                        veh.current_node = 'Node1'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)

                        Node1.vehicles.pop(0)
                        Node1.presence = False
                        Node1.time = 0
                        Exited_east.vehicles.append(veh.ID)
                        Exited_east.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                        #print(f"For {veh.origin} to {veh.destination}\n")
                        print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to east at time {Exited_east.time}")
                        veh.current_node = 'Exited_east'
                        veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                        time.sleep(node_headway_seconds)
                        save_time(veh)
                        break

            if veh.destination == 'south':
                if incoming[0].ID == veh.ID:
                    incoming.pop(0)
                    Exited_south.vehicles.append(veh.ID)
                    Exited_south.time = datetime.datetime.now().strftime("%I:%M:%S %p")
                    #print(f"For {veh.origin} to {veh.destination}\n")
                    print(f"\nVehicle {veh.ID} (going {veh.origin} to {veh.destination}) exited to (right turn) south at time {Exited_south.time}")
                    veh.current_node = 'Right_Exited_South'
                    veh.time=datetime.datetime.now().strftime("%I:%M:%S %p")
                    time.sleep(node_headway_seconds)
                    save_time(veh)
                    break
       
        # Check if all vehicles have been processed
        if not incoming:
            break
    #print(x11)  # prints all 6 time values      
        
            #incoming.pop(0)

#print("@@@@@@@@@@@@@@@@@", y_axis_time)

all_conflict_threads=[] 
# all vehicles in intersection move concurrently (vehicles remain in SO, NR.. lanes), but move between node classes
for i in all_queues:
    thread_conflict_movement= threading.Thread(target=define_Nodes, args=(i,))
    all_conflict_threads.append(thread_storage_movement)
    thread_conflict_movement.start()
    

# waits for all the threads in concflict zone to join, to indicate the vehicles have exited teh intersection 
for thread in all_conflict_threads:
    thread.join()
    

#print("@@@@@@@@@@@@@@@@@", y_axis_time)

###################################### MALICIOUS #####################################################################

# generate_fixed_imposter_ID()
# for veh in queue_order_NSEW:
#     accumulate_to_lanes()
