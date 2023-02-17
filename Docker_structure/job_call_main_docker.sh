#Call script arguments: /home/test_images/   50       30
#                       ${1}                 ${2}     ${3}

# Move to the folder containing the Raw images
cd /home/test_images/

######################################
#####    STrack cell tracking    #####
######################################

echo "Tracking cells using STrack"

# Create folder for STrack outputs
mkdir -p /home/test_images/STrack/
strack_dir="/home/test_images/STrack/"

MAXDIST=${2}
MAXANGLE=${3}
export MAXDIST
export MAXANGLE

# Launch script to extract features
python3 /home/scripts/strack_script_v4.py $MAXDIST $MAXANGLE ${strack_dir}

# Launch script to merge all STrack result tables into one csv file
python3 -W ignore /home/scripts/strack_merge_tables.py ${strack_dir}
