# Udacity Self-Driving Car Nanodegree

## Final Capstone Project - Writeup

---
[//]: # (Image References)

[image1]: ./writeup_images/av_architecture.png "Self Driving Car Architecture"
[image2]: ./writeup_images/ros_architecture.png "ROS Architecture"


This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. This is a team project in which we built parts of the individual systems of perception, planning and control and integrated them into one system using Robot Operating System(ROS).

For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

So, first let's get to know the team - 3 engineers from Bucharest to Bangalore to Taipei!

## The Team

1. Vijay Alagappan Alagappan (Team Lead) 

Vijay is a mechanical engineer by educational background and currently works as a crash safety engineer churning out simulations at Mercedes-Benz R&D from the Silicon Valley of India, Bangalore. He loves building stuff and making things work - your typical engineer!
Udacity Student Hub Display Name: Vijay Alagappan
Udacity account Email id: a.vijay.alagappan@gmail.com

2. Kevin Chiu 

Kevin's a software engineer who writes driver and software utilities, and still goes to office in these days of the Coronavirus! He is from one of Asia's richest and high-tech modern cities - Taipei(Taiwan). He works at day and does Udacity courses at night, and dreams to be a self-driving car engineer one day!
Udacity Student Hub Display Name: Kevin Chiu
Udacity account Email id: chiukevin08@gmail.com

3. Vlad Negreanu

Vlad is a software engineer writing driver software and is currently locked down and working from home like Vijay. He comes from the 'Paris of the East' - the beautiful city of Bucharest (Romania). He spends his day time on work and several sleepless nights coding!
Udacity Student Hub Display Name: Vlad N
Udacity account Email id: vnegreanu@yahoo.com

Now, lets get to the part on how to install required software and get things running..


## Installation, Usage and System Details

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the "uWebSocketIO Starter Guide" found in the classroom (see Extended Kalman Filter Project lesson).

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

### Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|        | Simulator | Carla  |
| :-----------: |:-------------:| :-----:|
| Nvidia driver | 384.130 | 384.130 |
| CUDA | 8.0.61 | 8.0.61 |
| cuDNN | 6.0.21 | 6.0.21 |
| TensorRT | N/A | N/A |
| OpenCV | 3.2.0-dev | 2.4.8 |
| OpenMP | N/A | N/A |

Yes, now that we are done with the chore of installations and knowing how to run the code, let us get to the fascinating part of programming autonomous vehicles!

## Project Overview 

This being the Capstone project required implementation of several topics that were introduced in the course. Th objective is to drive a lap on a car first on the simulator and then on Carla (the testing car provided by Udacity) obeying traffic signals. The driving route is given using a set of waypoints provided as input. There were primarily 4 areas on which we had to focus:

1. Perception

The perception part in a self driving car generally involves huge number of tasks ranging from simple detection of lanes and traffic signs to complex tasks such as detecting moving traffic, pedestrians, etc. using sensor fusion and localizing the vehicle. But, in this project, there were no moving traffic or pedestrians and no traffic signs. Finding lane lines and advanced localization was also not required, since we were provided with pre-programmed waypoints. We had to focus on only one task - which was detecting traffic signals and classifying the colour of the signal. So, that required 1. collecting or generating data, 2. trying out various object detection/classfication models and 3. infering/predicting in a short span of time so that the car does not skip signal while we let millions of weights flow through the deep neural network graph..

2. Planning

The topic of planning in a self driving car consists of high level tasks such as deciding the route from navigation systems to lower level tasks such as generating obstacle avoiding, jerk and acceleration minimizing trajectories based on input from the perception module. These have to be done keeping in mind the physical constraints such as the acceleration/deceleration limits, comfort levels, traffic safety rules such as speed limits, lane rules, etc. For the purpose of this project, we were not required to plan the main route. The main route was given in the form of waypoints (which don't change much due to zero obstacles on the road). We just had to generate trajectories in the form of modified subslices of these waypoints. So,these subslices of the original waypoints can be generated if we need know the closest waypoint to the current position of the vehicle. Then we can generate the trajectory starting from this waypoint. In addition, the waypoints now need to be modified so as to have zero velocities before red traffic signs. 

3. Control

Control is the topic closest to the hardware and the physics of vehicle motion. In a self-driving car, control algorithms are written to control primarily the three actuators - the brake, the steering and the throttle. This could be accomplished using anything, ranging from simple PID controllers to complex model based predictive controllers. In this project, we use a simple PID control for the throttle. For the steering, we use a model based yaw controller. We calculate the braking torque during motion based on the required deceleration and the brake torque during stops using the minimum torque limit required to keep the vehicle from rolling.

4. Integration

Integration is that last piece in the jigsaw puzzle of putting together a self driving car, which is solving that jigsaw puzzle itself! It involves coordination of signals coming in from the perception module, sending them to the planning module to get updated routes and trajectories and sending signals to the control module which eventually makes the hardware execute the commands. So, this requires coordination in space and most importantly time, so that signals don't get mixed up or sent in random order! In this project, the integration is done using the Robot Operating System - ROS which communicates with the Simulator or Carla the vehicle. We need to subscribe and publish topics on ros nodes to share information among the 3 modules.

Here's the pictorial flowchart representation of the architecture of a self driving car, showing an overview of the functions of each of these modules and the way they communicate with each other (Courtesy: [Udacity Self-Driving Car ND]())

![alt text][image1]

So, after the bird's overview let us zoom into the specific details:

## Implementation Details

### Perception

The perception module is implemented in the node `tl_detector`. It subscribes to the topics `current_pose`, `base_waypoints`, `vehicle/traffic_lights` and `image_color` to get the current position, the list of waypoints on the route, the list of traffic lights and the camera images respectively. It publishes to the topic `traffic_waypoint` the waypoint id of the next traffic light that is red.

**Code files:**
`tl_detector.py` : Checks where the vehicle is with respect to the list of traffic light stop lines; detects and classifies the traffic signal; is used for the simulator.
`tl_detector_site.py` : Does the same work as the previous file; is used for the site.
`tl_classifier.py` : Predicts the traffic light state using the deep learning prediction model trained on image data, and is called by the tl_detector.py with the current images from the camera passed to it; is used for the simulator.
`tl_classifier_site.py` : Does the same work as the previous file; is used for the site.
and some models : Multiple models trained on the generated image data. The folder named `model_02` contains the final trained model used for prediction in the simulator and the folder named `model_site_02` contains the final trained model used for prediction on the site.

### Planning

The planning module is implemented in the nodes `waypoint_loader` and `waypoint_updater`. For this project, the `waypoint_loader` was already provided and we had to write code only for the `waypoint_updater`. The waypoint updater subscribes to the topics `current_pose`, `base_waypoints` and `traffic_waypoint` to get the current position of the vehicle, the list of waypoints on the planned route and the waypoint id of the next traffic light in red state respectively. It publishes to the topic `final_waypoints` the final modified waypoints to stop the car before the traffic stop lines when the signal is red. 

**Code files:**
`waypoint_updater.py` : Reads the list of original waypoints and feeds them part by part to the final waypoints by slicing them based on the current position of the vehicle; modifies the velocities at each waypoint inorder to stop the vehicle before the red traffic lights.

### Control

The control module is implemented using the nodes `dbw_node` and `waypoint_follower`. The `waypoint_follower` node is already provided by Udacity and we are required only to work on the `dbw_node` node. It subscribes to the topics `current_velocity`, `twist_cmd` and `dbw_enabled` to get the current velocity of the vehicle, the target linear and angular velocities of the vehicle and the enabled/not-enabled status of the Drive-By-Wire respectively. It uses the controllers only if Drive-By-Wire is enabled and not if the vehicle is driven in manual mode to avoid accumulation of errors. It publishes the topics `steering_cmd`,`throttle_cmd` and `brake_cmd` which are used as commands to the vehicle hardware/simulator to move the vehicle accordingly.

**Code files:**
`dbw_node.py` : Gives out steering, throttle and brake commands based on the current velocities and target velocities using yaw controller for steering, PID controller for throttle and a simple model for braking. The controllers are used only if drive-by-wire is enabled.(Manual mode should be switched off) 
`twist_controller.py` : Calculates the throttle and brake based on PID control and simple mechanics.
`yaw_controller.py` : Calculates the steering command with steering angle and yaw rate calculations based on current and target linear and angular velocities.
`pid.py` : Gives out output command based on proportion, integral and derivative controller.
`lowpass.py` : Filters out high frequency noise of velocity values coming in from the vehicle sensors/simulator.

### Integration

The integration module is spread all throughout the project repo. It is implemented using ROS. Almost every file has code relevant to integration! Signals from perception module are sent to the planning module, signals from the planning module are sent to the control module and signals from the control module are sent to the hardware or simulator. So, there are multiple topics published and subscribed by several ROS nodes. This is best explained using this picture (source: [Udacity elf Driving Car ND](https://classroom.udacity.com/nanodegrees/nd013/parts/01a340a5-39b5-4202-9f89-d96de8cf17be/modules/702b3c5a-b896-4cca-8a64-dfe0daf09449/lessons/e43b2e6d-6def-4d3a-b332-7a58b847bfa4/concepts/455f33f0-2c2d-489d-9ab2-201698fbf21a)):

![alt text][image2]


## Results

The project rubric asks - "Did the car navigate the track successfully?" and specifies that "The submitted code must work successfully to navigate Carla around the test track." 

We checked the code on the simulator and found that it navigates succesfully around the test track. It stops within the stop line at red signals and then starts moving once again when it turns green. The max speed that we assigned to the vehicle in the simulator was 40kmph.

Before testing on Carla, we made the following preliminary checks:
1. The dbw_node works successfully on the test lot in the simulator with a max speed of 10kmph.
2. The tl_detector module also works good when it is tested with the rosbag video provided by Udacity.

We hope to see the code get reviewed on the simulator and also on Carla by Udacity. Overall, it was fun and a great learning experience. It gave all three of us the skills as well as the confidence required to code a self driving car.


