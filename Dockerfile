FROM ubuntu:16.04

# Install dependencies
RUN apt-get update
RUN apt-get -y install apache2

# Install apache and write hello world message
RUN echo 'Hello World!' > /var/www/html/index.html

# Configure apache
RUN echo '. /etc/apache2/envvars' > /root/run_apache.sh
RUN echo 'mkdir -p /var/run/apache2' >> /root/run_apache.sh
RUN echo 'mkdir -p /var/lock/apache2' >> /root/run_apache.sh
RUN echo '/usr/sbin/apache2 -D FOREGROUND' >> /root/run_apache.sh
RUN chmod 755 /root/run_apache.sh

EXPOSE 80

CMD /root/run_apache.sh



FROM python:3.6

WORKDIR /home/ec2-user
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/czhu505/hw3 /home/ec2-user/data622

EXPOSE 5000
CMD [ "json", "/home/ec2-user/data622/kaggle.json" ]
CMD [ "python", "/home/ec2-user/data622/pull_data.py" ]
CMD [ "python", "/home/ec2-user/data622/train_model.py" ]
CMD [ "python", "/home/ec2-user/data622/score_model.py" ]
