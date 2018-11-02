FROM ubuntu:18.04
FROM python:3.6-onbuild

RUN apt-get update &&apt-get upgrade -y&& apt-get install python-pip -y
RUN pip install --upgrade pip
RUN pip install numpy pandas sklearn matplotlib seaborn pyyaml 

WORKDIR /usr/local/bin

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/czhu505/hw3 /home/ubuntu/data622

#copy kaggle json file to root/.kaggle
copy kaggle.json /root/.kaggle

CMD [ "json", "/home/ubuntu/data622/kaggle.json" ]
CMD [ "python", "/home/ubuntu/data622/pull_data.py" ]
CMD [ "python", "/home/ubuntu/data622/train_model.py" ]
CMD [ "python", "/home/ubuntu/data622/score_model.py" ]
