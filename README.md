# STrack: a tool to Simply Track cells in your timelapse images

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/STrack/blob/master/cell_tracking.png">
</p>

To facilitate the installation and reproducible usability of STrack, we made a docker version of the package.

*Note: On this github page, we provided a few images from a timelapse that you can use as test images for STrack. In order to find them, scroll up to the top of this page and click on the green "Code" button and on "Download zip". The zipped folder that you will download contains a /test_images subfolder, containing cell masks that we obtained by using Omnipose (Kevin J. Cutler et al, 2021, [Omnipose](https://github.com/kevinjohncutler/omnipose.git)). You can of course use the segmentation tool of your choice to generate segmentation masks on your own images.*

## Here's a user-friendly step-by-step protocol to track cells in your images using STrack:

### Step 1: Install the Docker Desktop App

- **On Mac, Windows and Linux:** You will find the download link and instructions on this website: [Docker Desktop install](https://www.docker.com/products/docker-desktop/)

Once you have completed the installation, you can launch the Docker Desktop App

*Note: if you encounter issues with Docker Desktop on Windows, consider uninstalling it, restarting your computer, and re-installing Docker Desktop with admin rights, as explained on the docker forum (https://forums.docker.com/t/solved-docker-failed-to-start-docker-desktop-for-windows/106976).![image](https://user-images.githubusercontent.com/17719754/218061342-e727dca7-0ca3-4000-ab8a-615f1b2f1df7.png)*

### Step 2: Search for the helenatodd/strack image from the Docker Desktop App

In the docker Desktop App, <br />
(1) Click on the "Search" bar <br />
(2) Type "helenatodd/strack"

<p align="center">
  <img width="1000" height="500" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/search_helenatodd_strack.png">
</p>

(1) Then click on "Images" and <br />
(2) select the "helenatodd/strack:v1.1" docker image by clicking on it. <br />
(3) Finally, click on the "Run" button to launch the interface that will allow you to launch STrack on your segmented images.

<p align="center">
  <img width="1000" height="500" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/image_helenatodd_strack.png">
</p>

### Step 3: Run STrack on your images

First, click on the arrow next to "Optional settings" to access the settings of STrack (1):

<p align="center">
  <img width="1000" height="500" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/optsettings_helenatodd_strack.png">
</p>

You can now define the STrack parameters: <br />
(1) The first box can stay empty, it allows you to give a name to the container that will be launched, but docker will give it a default name if you don't. <br />
(2) By clicking on those three dots, you will be able to browse, on your computer, into the folder containing the segmented images in which you wish to track cells using STrack (or into the /test_images folder that we provided) <br />
(3) Type "/home/test_images/" in this box <br />
(4) Type "MAXDIST" in this box. This will allow you to define the maximum distance to look for descendance in a cell's surrounding <br />
(5) Type the maximum distance value you wish to set (as an example, we set this maximum distance to 50 pixels) <br />
(6) Click on the "+" button to enter a second parameter

<p align="center">
  <img width="1000" height="500" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/run_helenatodd_strack.png">
</p>

You can then provide information on the second STrack parameter: <br />
(1) Type "MAXANGLE" in this box. This will allow you to define the maximum angle allowed for cell division <br />
(2) Type the maximum angle value you wish to set (as an example, we set this maximum angle to 30°) <br />
(3) Finally, you can hit the "Run" button to launch STrack on your data <br />

<p align="center">
  <img width="1000" height="500" src="https://github.com/Helena-todd/STrack/blob/master/readme_images/run_helenatodd_strack2.png">
</p>

### STrack results

After running STrack on your segmented images, a new STrack subfolder will be generated in the folder where your images are located, that contains STrack's results. For each image - 1 (the cells in the 1st image cannot be tracked by definition), STrack returns: <br />
- a CSV table, that contains the links from cells in the previous to cells in the current image <br />
- a PNG image, in which these links are represented as red lines

STrack will also return two additional csv files:
- the "complete_tracking_table" contains tracks from all timepoints combined
- the "tracked_cells_table" contains information on cells from all timpoints combined

These two last CSV files can be used to import STrack's results into an open source software for visualizing and editing networks. We provide a tutorial on how to import STrack's results into Cytoscape, and how to visualise and/or edit the tracks, here: <a href="https://github.com/Helena-todd/STrack/blob/master/1_R_Intro.html">my text</a>








