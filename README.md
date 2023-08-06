# JayRadar

Jayradar is an open-source python vision pipeline program. It allows the user to create, edit, tune, save, and load pipelines using an array of interfaces and pipes.

Our pipeline is inspired by PhotonVision’s description of a pipeline:  

“A vision pipeline represents a series of steps that are used to acquire an image, process it, and analyzing it to find a target. In most FRC games, this means processing an image in order to detect a piece of retroreflective tape or an AprilTag.” 

The data for the pipeline is sourced from a camera that captures frames and timestamps each frame. These data sources can be customized for individual devices to optimize native hardware capabilities. 

The vision pipeline comprises a series of data pipes, each responsible for applying specific transformations to frames and corresponding data. For instance, filters are utilized to adjust the color balance of frames by modifying the red, green, and blue channels. Our project primarily focuses on a YOLOv8-based filter or the Ultralytics library, which leverages pretrained models in the yolov8 architecture. This filter effectively detects objects and includes only a single detection, subsequently adding the data back into the pipeline. 

As the data progresses through the various pipes, it ultimately reaches the output stage of the pipeline. Here, the data is posted to the network tables for FIRST Robotics Teams. Additionally, the frames can be locally displayed or transmitted to a web server from this section of the pipeline. 

The advantage of this approach lies in the flexibility and simplicity of the pipeline architecture. Creating a new source, pipe, or output is as straightforward as creating a child of the base class. This standardized template ensures clarity and ease for future implementations of sources, pipes, and outputs. 

# Installation

For device specific installation, visit the github wiki pages.

Otherwise, dependencies can be installed with:

```bash
cd ./api
pip install -r requirements.txt
```

And the frontend needs to be built with

```bash
cd ./client
npm install
npm run build
```

Assuming no dependency issues, you should be able to run the program with

```bash
cd ./api
python ./main.py
```
