# STrack: a tool to Simply Track cells in your timelapse images

![Cell tracking](https://github.com/Helena-todd/STrack/cell_tracking.png)
![Cell tracking](https://github.com/Helena-todd/STrack/blob/master/cell_tracking.png?raw=true)

To facilitate the installation and reproducible usability of STrack, we made a docker version of the package.

### Here's a user-friendly step-by-step protocol to track cells in your images using docker-STrack:

#### Step 1: Install the Docker Desktop App

- **On Mac:** You will find the download link and instructions on this website: [Docker Desktop Mac install](https://docs.docker.com/desktop/mac/install/)
- **On Windows:** You will find the download link and instructions on this website: [Docker Desktop Windows install](https://docs.docker.com/desktop/windows/install/)

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

Move to the STrack/Docker_structure directory on your computer by typing "cd" followed by the path to the directory:
- **On Mac:** 
> cd path_to_STrack/Docker_structure_directory
(e.g. cd /Users/Helena/Documents/STrack/Docker_structure)
- **On Windows:** 
> cd path_to_STrack/Docker_structure_directory
(e.g. cd C:\Users\Helena\Documents\STrack\Docker_structure)

Build the image by typing:
> docker build . –t strack

The docker App should now start building the docker image on your computer. 
(if not, make sure that you did not forget to launch the Docker Desktop App)

After a while, (this process can take a few minutes), all the steps should be completed. Your STrack docker image is now ready to use!

#### Step 4: Use docker-STrack to track cells in the test images

STrack takes 3 parameters as input:
- the path to the segmented images
- the maximum distance to look for descendance in a cell's surrounding (we set this maximum distance to 50 pixels)
- the maximum angle allowed for cell division (we set this maximum angle to 30°)

Now that you have built the docker-STrack image, you can use it to track cells in images, by typing:
- **On Mac:** 
> docker run -v path_to_test_images:/home/test_images/ strack /home/test_images/ 50 30
(e.g. docker run -v /Users/Helena/Documents/STrack/test_images/:/home/test_images/ strack /home/test_images/ 50 30)
- **On Windows:** 
> docker run -v path_to_test_images:/home/test_images/ strack /home/test_images/ 50 30
(e.g. docker run -v C:\Users\Helena\Documents\STrack\Docker_structure\:/home/test_images/ strack /home/test_images/ 50 30)

The -v option allows you to couple a folder on your local computer to a folder in the docker image. STrack's results will thus be directly outputted in the path you provided, in an /STrack subfolder.

After running the docker run command, a new STrack subfolder will be generated, that contains STrack's results. For each image - 1 (the cells in the 1st image cannot be tracked by definition), STrack returns:
- a CSV table, that contains the links from cells in the previous to cells in the current image
- a PNG image, in which these links are represented as red lines









