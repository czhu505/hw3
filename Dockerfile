FROM python:3.6

WORKDIR /home/ec2-user
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/czhu505/hw3 /home/ec2-user/data622

EXPOSE 5000
CMD [ "python", "/home/ec2-user/data622/pull_data.py" ]
CMD [ "python", "/home/ec2-user/data622/train_model.py" ]
CMD [ "python", "/home/ec2-user/data622/score_model.py" ]
