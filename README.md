# University of Pittsburgh INFSCI 2440 Artificial Intelligence Spring 2023 Final Project
## Optimal Routing of Packets Using RL

### Environment
The agent is the transmitter of traffic in our concept, and its activities lead to changes in sending rates.
We use the concept of monitor intervals (MIs) to define this.
Time is split into segments that are successive. 
The sender can alter its transmission rate xt at the start of each MI t, which remains constant during the MI.

### Sample Run
![video](sample_run.gif)
### Overview
This repo contains the gym environment required for training reinforcement
learning models for created policies that govern packet routing over a network with 2 routers and multiple senders


### Training
To run training only, go to ./src/gym/, install any missing requirements for
stable\_solve.py and run that script.

### Results

