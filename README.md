# STrack: a tool to Simply Track cells in your timelapse images

To facilitate the installation and reproducible usability of STrack, we made a docker version of the package.

### Here's a user-friendly step-by-step protocol to track cells in your images using docker-STrack:

#### Step 1: Install the Docker Desktop App

- **On Mac:** You will find the download link and instructions on this website: [Docker Desktop Mac](https://docs.docker.com/desktop/mac/install/)
- **On Windows:** You will find the download link and instructions on this website: [Docker Desktop Windows](https://docs.docker.com/desktop/windows/install/)

Once you have completed the installation, you can lauch the Docker Desktop App

#### Step 2: Dowlnoad docker-STrack on your computer

Git clone or download the Helena-todd/STrack repository.

You should now have an STrack folder on your computer. This folder contains:
- A Docker_structure sub-folder. Everything necessary to build the STrack docker image is stored there.
- A test_images/exported subfolder. We provided a few images from a timelapse to help you test STrack. These images contain cell masks, which we obtained by using Omnipose (Kevin J. Cutler et al, 2021, [Omnipose](https://github.com/kevinjohncutler/omnipose.git)). You can of course use the segmentation tool of your choice to generate segmentation masks.

#### Step 3: Build the STrack docker image on your computer

Open a command line:
- **On Mac:** you will find it in your Applications/Utilities/Terminal
- **On Windows:** you will find it by typing "Command Prompt" in the Power User Menu

Move to the STrack directory on your computer by typing:
- **On Mac:** 
    git







