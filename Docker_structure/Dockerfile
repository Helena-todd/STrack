FROM python:3.8-bullseye
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -U scikit-image
# install cv2
RUN pip install opencv-python
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -U scikit-learn
# install pandas
RUN pip3 install pandas
# install matplotlib
RUN pip install matplotlib
COPY job_call_main_docker.sh /home/scripts/
COPY strack_script_v4.py /home/scripts/
ENTRYPOINT ["bash", "/home/scripts/job_call_main_docker.sh"]
