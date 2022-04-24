# Yolo-Detection-In-Unity-Environment
Using the yolo neural net via python's cv2 inside a unity environment by passing through the camera through a udp socket.

* [Setup & Requirements](README.md#setup--requirements)
* [Usage](README.md#usage)
* [References and Appreciation](README.md#references-and-appreciation)

## Setup & Requirements
**Requirements**
- Unity Engine (tested on 2020.3.30f1)
- Python 3

<br/>

**Setup**
1. Download the weights from releases and place them in their respective folders `./YoloPythonServer/2ClassesTrained` and `./YoloPythonServer/12ClassesTrained`.

2. Create a Unity project and move the folders from `./UnityEnvironment` to their matching counterparts inside the project.  You may need to use operating system's file explorer to find the corresponding folders.  Unity's browser is limited to `Packages` and `Assets`.
    * i.e. move the content of the Assets in the github repository into Unity's Assets folder

3. install the Python dependencies found in `./YoloPythonServer/requirements.txt`.
    * i.e. `pip3 install -r requirements.txt`

4. (Optional) For improved speeds when using Yolo:  Instead of using the precomiled cv2 packages, compile your own with CUDA and cuDNN (Nvidia Only) and install the neccessary drivers.

<br/>

## Usage

- In the unity project, select the VirtualEnv.unity scene.  Start/ Run the scene.
- Run `./YoloPythonServer/server-stream-detect.py`

<br/>

## References and Appreciation
Unity Fly Cam: https://assetstore.unity.com/packages/tools/camera/free-fly-camera-140739

UDP Socket Networking Boiler Code: https://github.com/Siliconifier/Python-Unity-Socket-Communication

3D-Model-to-AI-Training-Data: https://github.com/clee93/3D-Model-to-AI-Training-Data
