FROM python

COPY /install-checkbandwidth.sh /root/
RUN /bin/bash /root/install-checkbandwidth.sh

#minutes
ENV INTERVAL=30

COPY check_bandwidth.py /root/
RUN chmod +x /root/check_bandwidth.py
RUN mkdir /root/config

COPY start-checkbandwidth /root/
RUN chmod +x /root/start-checkbandwidth
CMD ["/root/start-checkbandwidth"]
