import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


group_size_vs_del_time = {'2': [], '3': [], '4': []}

lambda_vs_del_time = {'2': [], '3': [], '5': []}

group_size_vs_efficiency = {'2': [], '3': [], '4': []}

lambda_vs_efficiency = {'2': [], '3': [], '5': []}


def plot_group_size_versus_avg_del_time(data):
	raw_data = []
	for k in sorted(data.keys()):
		raw_data.append(np.array(data[k]))

	raw_data = np.array(raw_data)
	means = [np.mean(raw_data[0]), np.mean(raw_data[1]), np.mean(raw_data[2])]
	stds = [np.std(raw_data[0]), np.std(raw_data[1]), np.std(raw_data[2])]

	print "Group size vs Avg. stable del. time"
	print "Means:", means
	print "Stds: ", stds
	print "\n"

	gs_2_axis = np.linspace(means[0] - 3 * stds[0], means[0] + 3 * stds[0], 10)
	gs_3_axis = np.linspace(means[1] - 3 * stds[0], means[1] + 3 * stds[1], 10)
	gs_4_axis = np.linspace(means[2] - 3 * stds[0], means[2] + 3 * stds[2], 10)
	x_axis = [2, 3, 4]

	plt.title("Group size vs Avg. stable del. time")
	plt.xlabel("Group size (# of nodes)")
	plt.ylabel("Avg. del. time (sec)")
	graph = plt.boxplot([gs_2_axis, gs_3_axis, gs_4_axis], labels=x_axis)
	graph['boxes'][0].set_color('red')
	graph['boxes'][1].set_color('green')
	graph['boxes'][2].set_color('blue')
	#plt.plot(means, "bo")
	plt.legend([graph['boxes'][0], graph['boxes'][1], graph['boxes'][2]], ['Size: 2', 'Size: 3', 'Size: 4'])
	plt.show()

def plot_group_size_versus_efficiency(data):
	raw_data = []
	for k in sorted(data.keys()):
		raw_data.append(np.array(data[k]))

	raw_data = np.array(raw_data)
	means = [np.mean(raw_data[0]), np.mean(raw_data[1]), np.mean(raw_data[2])]
	stds = [np.std(raw_data[0]), np.std(raw_data[1]), np.std(raw_data[2])]

	print "Group size vs Efficiency"
	print "Means:", means
	print "Stds: ", stds
	print "\n"

	gs_2_axis = np.linspace(means[0] - 3 * stds[0], means[0] + 3 * stds[0], 10)
	gs_3_axis = np.linspace(means[1] - 3 * stds[0], means[1] + 3 * stds[1], 10)
	gs_4_axis = np.linspace(means[2] - 3 * stds[0], means[2] + 3 * stds[2], 10)
	x_axis = [2, 3, 4]

	plt.title("Group size vs Efficiency")
	plt.xlabel("Group size (# of nodes)")
	plt.ylabel("Efficiency (%)")
	graph = plt.boxplot([gs_2_axis, gs_3_axis, gs_4_axis], labels=x_axis)
	graph['boxes'][0].set_color('red')
	graph['boxes'][1].set_color('green')
	graph['boxes'][2].set_color('blue')
	#plt.plot(x_axis, means, "bo")
	plt.legend([graph['boxes'][0], graph['boxes'][1], graph['boxes'][2]], ['Size: 2', 'Size: 3', 'Size: 4'])
	plt.show()

def plot_lambda_versus_avg_del_time(data):
	raw_data = []
	for k in sorted(data.keys()):
		raw_data.append(np.array(data[k]))

	raw_data = np.array(raw_data)
	means = [np.mean(raw_data[0]), np.mean(raw_data[1]), np.mean(raw_data[2])]
	stds = [np.std(raw_data[0]), np.std(raw_data[1]), np.std(raw_data[2])]

	m = list(means)
	m.reverse()
	s = list(stds)
	s.reverse()

	print "Lambda vs Avg. stable Del. time"
	print "Means:", m
	print "Stds: ", s
	print "\n"

	lb_2_axis = np.linspace(means[2] - 3 * stds[2], means[2] + 3 * stds[2], 10)
	lb_3_axis = np.linspace(means[1] - 3 * stds[1], means[1] + 3 * stds[1], 10)
	lb_5_axis = np.linspace(means[0] - 3 * stds[0], means[0] + 3 * stds[0], 10)
	x_axis = [2, 3, 5]

	plt.title("Lambda vs Avg. stable Del. time")
	plt.xlabel("Lambda (packets/sec)")
	plt.ylabel("Avg. del. time (sec)")
	graph = plt.boxplot([lb_2_axis, lb_3_axis, lb_5_axis], labels=x_axis)
	graph['boxes'][0].set_color('red')
	graph['boxes'][1].set_color('green')
	graph['boxes'][2].set_color('blue')
	#plt.plot(x_axis, means, "bo")
	plt.legend([graph['boxes'][0], graph['boxes'][1], graph['boxes'][2]], ['Lambda: 2', 'Lambda: 3', 'Lambda: 5'])
	plt.show()

def plot_lambda_versus_efficiency(data):
	raw_data = []
	for k in sorted(data.keys()):
		raw_data.append(np.array(data[k]))

	raw_data = np.array(raw_data)
	means = [np.mean(raw_data[0]), np.mean(raw_data[1]), np.mean(raw_data[2])]
	stds = [np.std(raw_data[0]), np.std(raw_data[1]), np.std(raw_data[2])]

	m = list(means)
	m.reverse()
	s = list(stds)
	s.reverse()

	print "Lambda vs Efficiency"
	print "Means:", m
	print "Stds: ", s
	print "\n"

	lb_2_axis = np.linspace(means[2] - 3 * stds[2], means[2] + 3 * stds[2], 10)
	lb_3_axis = np.linspace(means[1] - 3 * stds[1], means[1] + 3 * stds[1], 10)
	lb_5_axis = np.linspace(means[0] - 3 * stds[0], means[0] + 3 * stds[0], 10)
	x_axis = [2, 3, 5]

	plt.title("Lambda vs Efficiency")
	plt.xlabel("Lambda (packets/sec)")
	plt.ylabel("Efficiency (%)")
	graph = plt.boxplot([lb_2_axis, lb_3_axis, lb_5_axis], labels=x_axis)
	graph['boxes'][0].set_color('red')
	graph['boxes'][1].set_color('green')
	graph['boxes'][2].set_color('blue')
	#plt.plot(x_axis, means, "bo")
	plt.legend([graph['boxes'][0], graph['boxes'][1], graph['boxes'][2]], ['Lambda: 2', 'Lambda: 3', 'Lambda: 5'])
	plt.show()

if __name__ == '__main__':

	total_count_normal = 0
	total_count_lambda = 0

	for i in xrange(5):
		stat_file = 'output%d.txt' % (i + 1)

		with open(stat_file, 'r') as reader:
			current_group_size = None
			current_lambda = 2

			current_count = None
			current_upay = None
			current_tpay = None
			current_ttime = None
			current_atime = None

			end_flag = False
			lambda_flag = False
			i = 1

			exp_read = False

			for line in reader:

				if 'PPN' in line:
					comma_split = line.split(',')
					colon_split = map(lambda x: x.split(':'), comma_split)
					current_group_size = colon_split[1][1][-5]
					exp_read = False

				elif 'Count' in line:
					colon_split = line.split(':')
					current_count = int(colon_split[1])
					exp_read = False

					if not lambda_flag:
						total_count_normal += current_count

					else:
						total_count_lambda += current_count

				elif 'Useful' in line:
					colon_split = line.split(':')
					current_upay = float(colon_split[1])
					exp_read = False

				elif 'Total pay' in line:
					colon_split = line.split(':')
					current_tpay = float(colon_split[1])
					exp_read = False

				elif 'Avg' in line:
					colon_split = line.split(':')
					current_atime = float(colon_split[1])
					exp_read = True

				elif 'END' in line:
					end_flag = True

				elif 'LAMBDA' in line:
					lambda_flag = True
					i = 1

				else:
					continue

				if exp_read:

					if not lambda_flag:
						group_size_vs_del_time[current_group_size].append(current_atime)
						group_size_vs_efficiency[current_group_size].append(current_tpay / current_upay)

					else:
						lambda_vs_del_time[str(current_lambda)].append(current_atime)
						lambda_vs_efficiency[str(current_lambda)].append(current_tpay / current_upay)
						i += 1

						if i < 10:
							current_lambda = 2

						elif 10 <= i < 20:
							current_lambda = 3

						else:
							current_lambda = 5

					exp_read = False

	plot_group_size_versus_avg_del_time(group_size_vs_del_time)
	plot_lambda_versus_avg_del_time(lambda_vs_del_time)
	plot_group_size_versus_efficiency(group_size_vs_efficiency)
	plot_lambda_versus_efficiency(lambda_vs_efficiency)

	print "Total packets normal:", total_count_normal
	print "Total packets lambda:", total_count_lambda
