# CENG532-DistributedComputing-Project
*****************************************************************

**Contributors**: 
* burakceng (Burak Hocaoglu, 2035988)
* robofoxy (M. Rasit Ozdemir, 1942606)

This repo is built for the Term Project of the course CENG532 - Distributed Computing Systems offered by Department of Computer Engineering at Middle East Technical University (METU), Ankara, TURKEY.

The aim of the project is to design a reliable multicast (or atomic broadcast) protocol/algorithm that aims to solve the naturally impossible problem of establishing a coordination and consensus over an asynchronously operating P2P network. The aim is to solve the problem by making assumptions and restricting the solution space so that the complexity of the problem is reduced to a feasible level. Whole projevt is designed for the distributed network simulation environment **Mininet**. The project makes use of Mininet's Python API and the actual source code consists of Python language.

For technical and design details, experiment types and results, please refer to the report located in *CENG532-ProjectReport* directory

**To Experiment**:
* Make sure Mininet is properly installed into your computer or VM etc. For this, please refer to http://mininet.org/.
* USAGE: in Mininet's terminal type **sudo python script.py < # of packets per node > < topology type > < period > < lambda >**
* Tips for usage:
	* # of packets per node: e.g. if given 5, each node/process will multicast 5 messages (in total of 5x5 = 25 messages will be multicasted, excluding ACKs and delivery requests)
	* topology type: there are 3 types described in the project report changing in number of neighbours per node, refer to the *configurationX.xml* files and just give the number of it, e.g. if configuration3.xml is decided, just type 3.
	* period: the period of nodes multicasting their messages or the delay between 2 multicast procedures, under normal circumstances nodes will use this period
	* lambda: If you decide to experiment with uniform period, type **None** for lambda; otherwise, for poisson distributed multicast delays, enter a positive value here and please try to be feasible with it as poisson distribution can cause with very big delays

Finally, the experiments are limited to run only 5 minutes per node, when the 5-minute time is expired, the processes that run the nodes will be killed and after that point an extra of 30 seconds will be used for the Mininet script to tidy up what has obtained from that run and write the results into files *outputX.txt*, where X indicates the number/id of the node that generated that result.
