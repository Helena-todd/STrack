#Call script arguments: /home/test_images/   50       30
#                       ${1}                 ${2}     ${3}

# Move to the folder containing the Raw images
cd ${1}/exported/

######################################
#####    STrack cell tracking    #####
######################################

echo "Tracking cells using STrack "

# Create folder for STrack outputs
mkdir -p ${1}/STrack/
strack_dir="${1}/STrack/"

# Launch script to extract features
python3 /home/scripts/strack_script_v4.py ${2} ${3} ${strack_dir}
