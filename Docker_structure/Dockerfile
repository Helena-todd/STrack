# source image
FROM python:3.8-bullseye
# update the package of the source image
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir --upgrade pip
# install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# copy strack files
COPY job_call_main_docker.sh strack_script_v4.py strack_merge_tables.py /home/scripts/
# set how will be used the container when run
ENTRYPOINT ["bash", "/home/scripts/job_call_main_docker.sh"]
