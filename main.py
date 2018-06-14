import math
import datetime, time
import objects as ob

## Temp Test Functions ##

def move_linear_platform():
	print ("linear platform moved")

def reset_linear_platform():
	print ("linear platform reset")

def take_picture():
	print ("pictures taken")
	# print ("pictures stored")

def rotate_vial(interval):
	print ("vial rotated by", interval)

## ------------------- ##

def input_cmd(): ## returns object with parameters
	n_vials = int(input("Number of Vials (6 or less): "))
	steps = int(input("Number of pictures per vial: "))
	time = float(input("Length of Operation (mins): "))
	n_reps = int(input("Number of repetitions in length of operation: "))

	return ob.Operation_Input(n_vials, steps, time, n_reps)


def operation(input_ob):
	n_vials = input_ob.n_vials
	steps = input_ob.steps
	time = input_ob.time
	n_reps = input_ob.n_reps
	interval = math.floor(200 / steps)

	for i in range(n_vials):
		for j in range(steps):
			take_picture()
			rotate_vial(interval)
		if i == n_vials - 1:
			reset_linear_platform()
		else:
			move_linear_platform()	
	print ("rep complete")

def main():
	input_ob = input_cmd()
	periodic_scheduler = ob.Periodic_Scheduler(input_ob)
	periodic_scheduler.setup(60.0 * input_ob.time / float(input_ob.n_reps), operation, input_ob)
	periodic_scheduler.run()

if __name__ == '__main__':
	main()