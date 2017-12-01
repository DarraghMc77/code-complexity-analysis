FROM python:3.6.1

RUN apt-get update
RUN apt-get -y install wget \
	cmake \
	gcc \
	git

RUN wget https://github.com/libgit2/libgit2/archive/v0.26.0.tar.gz && \
tar xzf v0.26.0.tar.gz && \
cd libgit2-0.26.0/ && \
cmake . && \
make && \
make install

RUN ldconfig

WORKDIR /Users/Darragh/College/ScalableComputing/code-complexity-analysis/manager/
ADD . /Users/Darragh/College/ScalableComputing/code-complexity-analysis/manager/

# add requirements (to leverage Docker cache)
ADD ./requirements.txt requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD worker.py /

# run server
CMD python worker.py