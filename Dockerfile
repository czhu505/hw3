FROM ubuntu:18.04
MAINTAINER "Andrei Maksimov"


RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libpng12-dev libhdf5-dev
    
RUN pip3 install --upgrade pip
RUN pip3 install tensorflow
RUN pip3 install numpy pandas sklearn matplotlib seaborn jupyter pyyaml h5py


RUN apt-get update; \
    apt-get -y upgrade
 
RUN apt-get -y install g++ cmake git subversion


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/czhu505/hw3 /home/ubuntu/data622.git -b master; 

#copy kaggle json file to root/.kaggle
copy kaggle.json /root/.kaggle

CMD [ "json", "/home/ubuntu/data622/kaggle.json" ]
CMD [ "python", "/home/ubuntu/data622/pull_data.py" ]
CMD [ "python", "/home/ubuntu/data622/train_model.py" ]
CMD [ "python", "/home/ubuntu/data622/score_model.py" ]


