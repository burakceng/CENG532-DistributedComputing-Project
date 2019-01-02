# GROUP 01
# Burak HOCAOGLU 2035988
# Baris BAYRAKTAR 2035715

# This file is to obtain statistics on the metrics and piont specified in the assignment text.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

########################## Read Data Files, Compute Mean & Standard Deviation ##########################

## Experiment 1
exp1_rdt_loss_01_data = np.loadtxt('data/rdt/exp1_rdt_loss_01.txt')
exp1_rdt_loss_5_data  = np.loadtxt('data/rdt/exp1_rdt_loss_5.txt')
exp1_rdt_loss_10_data = np.loadtxt('data/rdt/exp1_rdt_loss_10.txt')

exp1_sctp_loss_01_data = np.loadtxt('data/sctp/exp1_sctp_loss_01.txt')
exp1_sctp_loss_5_data  = np.loadtxt('data/sctp/exp1_sctp_loss_5.txt')

## Experiment 2
### Packet Loss
exp2_rdt_loss_01_data = np.loadtxt('data/rdt/exp2_rdt_loss_01.txt')
exp2_rdt_loss_5_data  = np.loadtxt('data/rdt/exp2_rdt_loss_5.txt')
exp2_rdt_loss_10_data = np.loadtxt('data/rdt/exp2_rdt_loss_10.txt')

exp2_sctp_loss_01_data = np.loadtxt('data/sctp/exp2_sctp_loss_01.txt')
exp2_sctp_loss_5_data  = np.loadtxt('data/sctp/exp2_sctp_loss_5.txt')

### Packet Corruption
exp2_rdt_corr_01_data = np.loadtxt('data/rdt/exp2_rdt_corr_01.txt')
exp2_rdt_corr_5_data  = np.loadtxt('data/rdt/exp2_rdt_corr_5.txt')
exp2_rdt_corr_20_data = np.loadtxt('data/rdt/exp2_rdt_corr_20.txt')

exp2_sctp_corr_01_data = np.loadtxt('data/sctp/exp2_sctp_corr_01.txt')
exp2_sctp_corr_5_data  = np.loadtxt('data/sctp/exp2_sctp_corr_5.txt')

### Packet Re-ordering
exp2_rdt_reor_5_data  = np.loadtxt('data/rdt/exp2_rdt_reo_5.txt')
exp2_rdt_reor_20_data = np.loadtxt('data/rdt/exp2_rdt_reo_20.txt')
exp2_rdt_reor_35_data = np.loadtxt('data/rdt/exp2_rdt_reo_35.txt')

exp2_sctp_reor_5_data  = np.loadtxt('data/sctp/exp2_sctp_reo_5.txt')
exp2_sctp_reor_20_data = np.loadtxt('data/sctp/exp2_sctp_reo_20.txt')
exp2_sctp_reor_35_data = np.loadtxt('data/sctp/exp2_sctp_reo_35.txt')

# -----------------------------------------------------------------------------


# Calculating means of each experiment data
exp1_rdt_loss_01_mean = np.mean(exp1_rdt_loss_01_data)
exp1_rdt_loss_5_mean  = np.mean(exp1_rdt_loss_5_data)
exp1_rdt_loss_10_mean = np.mean(exp1_rdt_loss_10_data)

exp1_sctp_loss_01_mean = np.mean(exp1_sctp_loss_01_data)
exp1_sctp_loss_5_mean  = np.mean(exp1_sctp_loss_5_data)

exp2_rdt_loss_01_mean = np.mean(exp2_rdt_loss_01_data)
exp2_rdt_loss_5_mean  = np.mean(exp2_rdt_loss_5_data)
exp2_rdt_loss_10_mean = np.mean(exp2_rdt_loss_10_data)

exp2_sctp_loss_01_mean = np.mean(exp2_sctp_loss_01_data)
exp2_sctp_loss_5_mean  = np.mean(exp2_sctp_loss_5_data)

exp2_rdt_corr_01_mean = np.mean(exp2_rdt_corr_01_data)
exp2_rdt_corr_5_mean = np.mean(exp2_rdt_corr_5_data)
exp2_rdt_corr_20_mean = np.mean(exp2_rdt_corr_20_data)

exp2_sctp_corr_01_mean = np.mean(exp2_sctp_corr_01_data)
exp2_sctp_corr_5_mean  = np.mean(exp2_sctp_corr_5_data)

exp2_rdt_reor_5_mean  = np.mean(exp2_rdt_reor_5_data)
exp2_rdt_reor_20_mean = np.mean(exp2_rdt_reor_20_data)
exp2_rdt_reor_35_mean = np.mean(exp2_rdt_reor_35_data)

exp2_sctp_reor_5_mean  = np.mean(exp2_sctp_reor_5_data)
exp2_sctp_reor_20_mean = np.mean(exp2_sctp_reor_20_data)
exp2_sctp_reor_35_mean = np.mean(exp2_sctp_reor_35_data)



# Calculating standard deviation of each experiment data
exp1_rdt_loss_01_std = np.std(exp1_rdt_loss_01_data)
exp1_rdt_loss_5_std  = np.std(exp1_rdt_loss_5_data)
exp1_rdt_loss_10_std = np.std(exp1_rdt_loss_10_data)

exp1_sctp_loss_01_std = np.std(exp1_sctp_loss_01_data)
exp1_sctp_loss_5_std  = np.std(exp1_sctp_loss_5_data)

## Experiment 2
### Packet Loss
exp2_rdt_loss_01_std = np.std(exp2_rdt_loss_01_data)
exp2_rdt_loss_5_std  = np.std(exp2_rdt_loss_5_data)
exp2_rdt_loss_10_std = np.std(exp2_rdt_loss_10_data)

exp2_sctp_loss_01_std = np.std(exp2_sctp_loss_01_data)
exp2_sctp_loss_5_std  = np.std(exp2_sctp_loss_5_data)

### Packet Corruption
exp2_rdt_corr_01_std = np.std(exp2_rdt_corr_01_data)
exp2_rdt_corr_5_std = np.std(exp2_rdt_corr_5_data)
exp2_rdt_corr_20_std = np.std(exp2_rdt_corr_20_data)

exp2_sctp_corr_01_std = np.std(exp2_sctp_corr_01_data)
exp2_sctp_corr_5_std  = np.std(exp2_sctp_corr_5_data)

### Packet Re-ordering
exp2_rdt_reor_5_std  = np.std(exp2_rdt_reor_5_data)
exp2_rdt_reor_20_std = np.std(exp2_rdt_reor_20_data)
exp2_rdt_reor_35_std = np.std(exp2_rdt_reor_35_data)

exp2_sctp_reor_5_std  = np.std(exp2_sctp_reor_5_data)
exp2_sctp_reor_20_std = np.std(exp2_sctp_reor_20_data)
exp2_sctp_reor_35_std = np.std(exp2_sctp_reor_35_data)



exp1_rdt_loss_01_x = np.linspace(exp1_rdt_loss_01_mean - 3 * exp1_rdt_loss_01_std, exp1_rdt_loss_01_mean + 3 * exp1_rdt_loss_01_std, 10)
exp1_rdt_loss_5_x  = np.linspace(exp1_rdt_loss_5_mean  - 3 * exp1_rdt_loss_5_std , exp1_rdt_loss_5_mean  + 3 * exp1_rdt_loss_5_std , 10)
exp1_rdt_loss_10_x = np.linspace(exp1_rdt_loss_10_mean - 3 * exp1_rdt_loss_10_std, exp1_rdt_loss_10_mean + 3 * exp1_rdt_loss_10_std, 10)

exp1_sctp_loss_01_x = np.linspace(exp1_sctp_loss_01_mean - 3 * exp1_sctp_loss_01_std, exp1_sctp_loss_01_mean + 3 * exp1_sctp_loss_01_std, 5)
exp1_sctp_loss_5_x  = np.linspace(exp1_sctp_loss_5_mean  - 3 * exp1_sctp_loss_5_std , exp1_sctp_loss_5_mean  + 3 * exp1_sctp_loss_5_std , 5)

exp2_rdt_loss_01_x = np.linspace(exp2_rdt_loss_01_mean - 3 * exp2_rdt_loss_01_std, exp2_rdt_loss_01_mean + 3 * exp2_rdt_loss_01_std, 10)
exp2_rdt_loss_5_x  = np.linspace(exp2_rdt_loss_5_mean  - 3 * exp2_rdt_loss_5_std , exp2_rdt_loss_5_mean  + 3 * exp2_rdt_loss_5_std , 10)
exp2_rdt_loss_10_x = np.linspace(exp2_rdt_loss_10_mean - 3 * exp2_rdt_loss_10_std, exp2_rdt_loss_10_mean + 3 * exp2_rdt_loss_10_std, 10)

exp2_sctp_loss_01_x = np.linspace(exp2_sctp_loss_01_mean - 3 * exp2_sctp_loss_01_std, exp2_sctp_loss_01_mean + 3 * exp2_sctp_loss_01_std, 5)
exp2_sctp_loss_5_x  = np.linspace(exp2_sctp_loss_5_mean  - 3 * exp2_sctp_loss_5_std , exp2_sctp_loss_5_mean  + 3 * exp2_sctp_loss_5_std , 5)

exp2_rdt_corr_01_x = np.linspace(exp2_rdt_corr_01_mean - 3 * exp2_rdt_corr_01_std, exp2_rdt_corr_01_mean + 3 * exp2_rdt_corr_01_std, 10)
exp2_rdt_corr_5_x  = np.linspace(exp2_rdt_corr_5_mean  - 3 * exp2_rdt_corr_5_std , exp2_rdt_corr_5_mean  + 3 * exp2_rdt_corr_5_std , 10)
exp2_rdt_corr_20_x = np.linspace(exp2_rdt_corr_20_mean - 3 * exp2_rdt_corr_20_std, exp2_rdt_corr_20_mean + 3 * exp2_rdt_corr_20_std, 10)

exp2_sctp_corr_01_x = np.linspace(exp2_sctp_corr_01_mean - 3 * exp2_sctp_corr_01_std, exp2_sctp_corr_01_mean + 3 * exp2_sctp_corr_01_std, 5)
exp2_sctp_corr_5_x  = np.linspace(exp2_sctp_corr_5_mean  - 3 * exp2_sctp_corr_5_std , exp2_sctp_corr_5_mean  + 3 * exp2_sctp_corr_5_std , 5)

exp2_rdt_reor_5_x   = np.linspace(exp2_rdt_reor_5_mean  - 3 * exp2_rdt_reor_5_std , exp2_rdt_reor_5_mean  + 3 * exp2_rdt_reor_5_std , 10)
exp2_rdt_reor_20_x  = np.linspace(exp2_rdt_reor_20_mean - 3 * exp2_rdt_reor_20_std, exp2_rdt_reor_20_mean + 3 * exp2_rdt_reor_20_std, 10)
exp2_rdt_reor_35_x  = np.linspace(exp2_rdt_reor_35_mean - 3 * exp2_rdt_reor_35_std, exp2_rdt_reor_35_mean + 3 * exp2_rdt_reor_35_std, 10)

exp2_sctp_reor_5_x   = np.linspace(exp2_sctp_reor_5_mean  - 3 * exp2_sctp_reor_5_std , exp2_sctp_reor_5_mean  + 3 * exp2_sctp_reor_5_std , 5)
exp2_sctp_reor_20_x  = np.linspace(exp2_sctp_reor_20_mean - 3 * exp2_sctp_reor_20_std, exp2_sctp_reor_20_mean + 3 * exp2_sctp_reor_20_std, 5)
exp2_sctp_reor_35_x  = np.linspace(exp2_sctp_reor_35_mean - 3 * exp2_sctp_reor_35_std, exp2_sctp_reor_35_mean + 3 * exp2_sctp_reor_35_std, 5)

x_axis = [1, 2, 3]



###################### PLOTS : To see them comment them out ##############################

"""
# Experiment 1 - Packet Loss
plt.suptitle('Experiment 1 - RDT & SCTP Packet Loss', fontsize=15)

# exp1_rdt_loss
labels_rdt = [0.1, 5, 10]
means_rdt = [exp1_rdt_loss_01_mean, exp1_rdt_loss_5_mean, exp1_rdt_loss_10_mean]

plt.subplot(1, 2, 1)
plt.title('RDT', fontsize=12)
plt.xlabel('Packet loss percentage')
plt.ylabel('File transfer time(sec)')
rdt = plt.boxplot([exp1_rdt_loss_01_x, exp1_rdt_loss_5_x, exp1_rdt_loss_10_x], labels=labels_rdt)
rdt['boxes'][0].set_color('red')
rdt['boxes'][1].set_color('green')
rdt['boxes'][2].set_color('blue')
plt.plot(x_axis, means_rdt)
plt.legend([rdt['boxes'][0], rdt['boxes'][1], rdt['boxes'][2]], ['Loss: 0.1%', 'Loss: 5%', 'Loss: 10%'], loc=2)

# exp1_sctp_loss
labels_sctp = [0.1, 5]
means_sctp = [exp1_sctp_loss_01_mean, exp1_sctp_loss_5_mean]

plt.subplot(1, 2, 2)
plt.title('SCTP', fontsize=12)
plt.xlabel('Packet loss percentage')
plt.ylabel('File transfer time(sec)')
sctp = plt.boxplot([exp1_sctp_loss_01_x, exp1_sctp_loss_5_x], labels=labels_sctp)
sctp['boxes'][0].set_color('red')
sctp['boxes'][1].set_color('green')
plt.plot(x_axis[:2], means_sctp)
plt.legend([sctp['boxes'][0], sctp['boxes'][1]], ['Loss: 0.1%', 'Loss: 5%'], loc=2)
"""


"""
# Experiment 2 - Packet Loss
plt.suptitle('Experiment 2 - RDT & SCTP Packet Loss', fontsize=15)

# exp2_rdt_loss
labels_rdt = [0.1, 5, 10]
means_rdt = [exp2_rdt_loss_01_mean, exp2_rdt_loss_5_mean, exp2_rdt_loss_10_mean]

plt.subplot(1, 2, 1)
plt.title('RDT', fontsize=12)
plt.xlabel('Packet loss percentage')
plt.ylabel('File transfer time(sec)')
rdt = plt.boxplot([exp2_rdt_loss_01_x, exp2_rdt_loss_5_x, exp2_rdt_loss_10_x], labels=labels_rdt)
rdt['boxes'][0].set_color('red')
rdt['boxes'][1].set_color('green')
rdt['boxes'][2].set_color('blue')
plt.plot(x_axis, means_rdt)
plt.legend([rdt['boxes'][0], rdt['boxes'][1], rdt['boxes'][2]], ['Loss: 0.1%', 'Loss: 5%', 'Loss: 10%'], loc=2)

# exp2_sctp_loss
labels_sctp = [0.1, 5]
means_sctp = [exp2_sctp_loss_01_mean, exp2_sctp_loss_5_mean]

plt.subplot(1, 2, 2)
plt.title('SCTP', fontsize=12)
plt.xlabel('Packet loss percentage')
plt.ylabel('File transfer time(sec)')
sctp = plt.boxplot([exp2_sctp_loss_01_x, exp2_sctp_loss_5_x], labels=labels_sctp)
sctp['boxes'][0].set_color('red')
sctp['boxes'][1].set_color('green')
plt.plot(x_axis[:2], means_sctp)
plt.legend([sctp['boxes'][0], sctp['boxes'][1]], ['Loss: 0.1%', 'Loss: 5%'], loc=2)
"""


"""
# Experiment 2 - Packet Corruption
plt.suptitle('Experiment 2 - RDT & SCTP Packet Corruption', fontsize=15)

# exp2_rdt_corr
labels_rdt = [0.1, 5, 20]
means_rdt = [exp2_rdt_corr_01_mean, exp2_rdt_corr_5_mean, exp2_rdt_corr_20_mean]

plt.subplot(1, 2, 1)
plt.title('RDT', fontsize=12)
plt.xlabel('Corruption percentage')
plt.ylabel('File transfer time(sec)')
rdt = plt.boxplot([exp2_rdt_corr_01_x, exp2_rdt_corr_5_x, exp2_rdt_corr_20_x], labels=labels_rdt)
rdt['boxes'][0].set_color('red')
rdt['boxes'][1].set_color('green')
rdt['boxes'][2].set_color('blue')
plt.plot(x_axis, means_rdt)
plt.legend([rdt['boxes'][0], rdt['boxes'][1], rdt['boxes'][2]], ['Corr.: 0.1%', 'Corr.: 5%', 'Corr.: 20%'], loc=2)

# exp2_sctp_corr
labels_sctp = [0.1, 5]
means_sctp = [exp2_sctp_corr_01_mean, exp2_sctp_corr_5_mean]

plt.subplot(1, 2, 2)
plt.title('SCTP', fontsize=12)
plt.xlabel('Corruption percentage')
plt.ylabel('File transfer time(sec)')
sctp = plt.boxplot([exp2_sctp_corr_01_x, exp2_sctp_corr_5_x], labels=labels_sctp)
sctp['boxes'][0].set_color('red')
sctp['boxes'][1].set_color('green')
plt.plot(x_axis[:2], means_sctp)
plt.legend([sctp['boxes'][0], sctp['boxes'][1]], ['Corr.: 0.1%', 'Corr.: 5%'], loc=2)
"""


"""
# Experiment 2 - Packet Re-ordering
plt.suptitle('Experiment 2 - RDT & SCTP Packet Re-ordering', fontsize=15)

# exp2_rdt_reor
labels_rdt = [5, 20, 35]
means_rdt = [exp2_rdt_reor_5_mean, exp2_rdt_reor_20_mean, exp2_rdt_reor_35_mean]

plt.subplot(1, 2, 1)
plt.title('RDT', fontsize=12)
plt.xlabel('Re-ordering percentage')
plt.ylabel('File transfer time(sec)')
rdt = plt.boxplot([exp2_rdt_reor_5_x, exp2_rdt_reor_20_x, exp2_rdt_reor_35_x], labels=labels_rdt)
rdt['boxes'][0].set_color('red')
rdt['boxes'][1].set_color('green')
rdt['boxes'][2].set_color('blue')
plt.plot(x_axis, means_rdt)
plt.legend([rdt['boxes'][0], rdt['boxes'][1], rdt['boxes'][2]], ['Reor.: 5%', 'Reor.: 20%', 'Reor.: 35%'], loc=1)

# exp2_sctp_reor
labels_sctp = [5, 20, 35]
means_sctp = [exp2_sctp_reor_5_mean, exp2_sctp_reor_20_mean, exp2_sctp_reor_35_mean]

plt.subplot(1, 2, 2)
plt.title('SCTP', fontsize=12)
plt.xlabel('Re-ordering percentage')
plt.ylabel('File transfer time(sec)')
sctp = plt.boxplot([exp2_sctp_reor_5_x, exp2_sctp_reor_20_x, exp2_sctp_reor_35_x], labels=labels_sctp)
sctp['boxes'][0].set_color('red')
sctp['boxes'][1].set_color('green')
sctp['boxes'][2].set_color('blue')
plt.plot(x_axis, means_sctp)
plt.legend([sctp['boxes'][0], sctp['boxes'][1], sctp['boxes'][2]], ['Reor.: 5%', 'Reor.: 20%', 'Reor.: 35%'], loc=2)
"""


plt.show()