# STrack: a tool to Simply Track cells in your timelapse images

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/cell_tracking.png">
</p>

To facilitate the installation and reproducible usability of STrack, we made a docker version of the package.

### Here's a user-friendly step-by-step protocol to track cells in your images using STrack:

#### Step 1: Install the Docker Desktop App

- **On Mac, Windows and Linux:** You will find the download link and instructions on this website: [Docker Desktop install](https://www.docker.com/products/docker-desktop/)

Once you have completed the installation, you can launch the Docker Desktop App

#### Step 2: Search for the helenatodd/strack image from the Docker Desktop App

In the docker Desktop App, click on the "Search" bar and type "helenatodd/strack":

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/search_helenatodd_strack.png">
</p>

Then click on "Images" (1) and select the "helenatodd/strack:v1.1" docker image by clicking on it (2). Finally, click on the "Run" button to launch the interface that will allow you to launch STrack on your segmented images.

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/image_helenatodd_strack.png">
</p>

Note: On this github page, we provided a few images from a timelapse that you can use as test images for STrack. In order to find them, scroll up to the top of this page and click on the green "Code" button and on "Download zip". The zipped folder that you will download contains a /test_images subfolder, containing cell masks that we obtained by using Omnipose (Kevin J. Cutler et al, 2021, [Omnipose](https://github.com/kevinjohncutler/omnipose.git)). You can of course use the segmentation tool of your choice to generate segmentation masks on your own images.

#### Step 3: Run STrack on your images

First, click on "Optional settings" to access the settings of STrack (1):

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/optsettings_helenatodd_strack.png">
</p>

You can now define the STrack parameters:
(1) The first box can stay empty, it allows you to give a name to the container that will be launched, but docker will give it a default name if you don't.
(2) By clicking on those three dots, you will be able to browse into the folder containing the segmented images in which you wish to track cells using STrack (or into the /test_images folder that we provided)
(3) Type "/home/test_images/" in this box
(4) Type "MAXDIST" in this box. This will allow you to define the maximum distance to look for descendance in a cell's surrounding 
(5) Type the maximum distance value you wish to set (as an example, we set this maximum distance to 50 pixels)
(6) Click on the "+" button to enter a second parameter

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/run_helenatodd_strack.png">
</p>

You can then provide information on the second STrack parameter:
(1) Type "MAXANGLE" in this box. This will allow you to define the maximum angle allowed for cell division
(2) Type the maximum angle value you wish to set (as an example, we set this maximum angle to 30°)
(3) Finally, you can hit the "Run" button to launch STrack on your data

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/run_helenatodd_strack2.png">
</p>

#### STrack results

After running STrack on your segmented images, a new STrack subfolder will be generated in the folder where your images are located, that contains STrack's results. For each image - 1 (the cells in the 1st image cannot be tracked by definition), STrack returns:
- a CSV table, that contains the links from cells in the previous to cells in the current image
- a PNG image, in which these links are represented as red lines







