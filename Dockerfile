FROM ubuntu:18.04
MAINTAINER "Andrei Maksimov"

COPY requirements.txt ./
RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libhdf5-dev
    
RUN pip3 install --upgrade pip
RUN pip3 install numpy pandas sklearn matplotlib seaborn jupyter pyyaml h5py

#copy kaggle json file to root/.kaggle
copy kaggle.json /root/.kaggle

WORKDIR /usr/src/app

CMD [ "pull_data.py", "train_model.py","score_model.py"  ]


