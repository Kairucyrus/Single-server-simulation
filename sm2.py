import math
import sys
import random

IDLE = 0
BUSY = 1
Q_LIMIT = 100


def initialize():
	global sim_time, server_status, num_in_que, time_last_event, time_next_event,\
	num_custs_delayed, total_delays, area_num_in_que, area_server_status

	num_custs_delayed = 0#statistical counters initialize<<>>
	total_delays = 0.0
	area_num_in_que = 0.0
	area_server_status = 0.0  

	sim_time = 0.0
	server_status = IDLE ##state variables initialize<<>>
	num_in_que = 0
	time_last_event = 0.0
	time_next_event = [0] * 3
	time_next_event[2] = 1.0e+30 #set to a very large value; no pending events at the beginning of the simulation


def timing():
	global next_event_type, sim_time

	min_time_next_event = 1.0e+29 #<<<initialized to a very large value to ensure first event is correctly identified
	next_event_type = 0

	for i in range(1, num_events + 1): #determine next event type
		if(time_next_event[i] < min_time_next_event):
			min_time_next_event = time_next_event[i]
			next_event_type = i
	if(next_event_type == 0): #is event list empty? check
		print(f"\nEvent list is empty at time (sim_time)")
		sys.exit(1) ##

	sim_time = min_time_next_event

def arrive():
	global sim_time, server_status, num_in_que, total_delays, num_custs_delayed
	
	time_next_event[1] = sim_time + expon(mean_interarrival)

	if (server_status == BUSY): #<<<<<
		num_in_que += 1
		if (num_in_que > Q_LIMIT): ##<<<
			print(f"\nOverflow of array time arrival at time {sim_time:.4f}")
			sys.exit(1)

		time_arrival[num_in_que] = sim_time

	else:
		delay = 0.0 ##<<<<<fl<<<<<
		total_delays += delay
		num_custs_delayed += 1

		server_status = BUSY

		time_next_event[2] = sim_time + expon(mean_service)##<<<<<<mean<<service

def depart():
	global sim_time, num_in_que, total_delays, num_custs_delayed, server_status
	if(num_in_que == 0):
		server_status = IDLE
		time_next_event[2] = 1.0e+30 #<

	else:
		num_in_que -= 1
		delay = sim_time - time_arrival[1] #<<<<<<<<<<<<<<<<<<<<<<<<
		total_delays += delay


		num_custs_delayed += 1
		time_next_event[2] = sim_time + expon(mean_service)

		for i in range(1, num_in_que + 1): #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
			time_arrival[i] = time_arrival[i + 1]

def report():
	global total_delays, num_custs_delayed, sim_time, area_num_in_que, area_server_status
	with open("mm1.out", "w") as outfile:
		outfile.write(f"** Single server queueing system ***\n\n"\
			f"Mean interarrival time: {mean_interarrival:.3f} \n"
			f"Mean service time: {mean_service:.3f} \n"
			f"Number of customers: {num_delays_required:.0f}"
			f"\nAverage delay in queue: {total_delays / num_custs_delayed:.3f} minutes\n\n"
			f"Average number in queue: {area_num_in_que/ sim_time:.3f}\n\n"
			f"Server utilization: {area_server_status / sim_time:.3f}\n\n"
			f"Time simulation ended: {sim_time:.3f} minutes"
			)



def main():
	with open("mm1.in", "r") as file:
		for line in file:
			global mean_interarrival, mean_service, num_delays_required
			mean_interarrival, mean_service, num_delays_required = map(float, line.split())

	#initializing the number of event types (arrival or departure)
	global num_events, time_arrival 
	num_events = 2
	time_arrival = [0] * (Q_LIMIT + 1)

	initialize() #initialize the simulation

	while (num_custs_delayed < num_delays_required):#<<<int<<<float<<<
		timing() #determine the next event
		update_time_avg_stats() #update the time-average statistical accumulators

		if next_event_type == 1: ##<<<<<<<<<<<<arrival | departure
			arrive()
		elif next_event_type == 2:
			depart()

	report()

def update_time_avg_stats():
	global time_last_event, area_num_in_que, area_server_status
	time_since_last_event = sim_time - time_last_event ##<<<<<<
	time_last_event = sim_time

	area_num_in_que += num_in_que * time_since_last_event

	area_server_status += server_status*time_since_last_event

def expon(mean):
	return -mean * math.log(random.random()) ##<<<<<transform a uniform random var from[0,1] to an exponential random var<<<<<<

if __name__ == "__main__":
	main()







