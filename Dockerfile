FROM ubuntu:bionic

RUN apt-get -y update

RUN apt-get install -y npm bash-completion sudo git

RUN useradd -m fragments
RUN usermod -aG sudo fragments
WORKDIR /home/fragments
ENV HOME /home/fragments
ENV PATH $PATH:$HOME/.local/bin
ENV LANG C.UTF-8

# Install Solidity v0.4.24
USER fragments
RUN mkdir -p /home/fragments/dependencies
WORKDIR /home/fragments/dependencies
RUN git clone https://github.com/ethereum/solidity.git
WORKDIR /home/fragments/dependencies/solidity
RUN git checkout v0.4.24
RUN git submodule update --init --recursive
USER root
RUN ./scripts/install_deps.sh
RUN ./scripts/build.sh

# BEGIN Requirements for Manticore:

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-pip

RUN apt-get install -y build-essential software-properties-common
USER fragments
RUN pip3 install manticore

# END Requirements for Manticore

# BEGIN Install Echidna

USER root
RUN apt-get install -y libgmp-dev libbz2-dev libreadline-dev curl software-properties-common locales-all locales libsecp256k1-dev
RUN curl -sSL https://get.haskellstack.org/ | sh
USER fragments
WORKDIR /home/fragments/dependencies
RUN git clone https://github.com/trailofbits/echidna.git
WORKDIR /home/fragments/dependencies/echidna
RUN stack upgrade
RUN stack setup
RUN stack install
WORKDIR /home/fragments

USER root

RUN update-locale LANG=en_US.UTF-8
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# END Install Echidna

USER fragments

COPY echidna /home/fragments/echidna/
COPY manticore /home/fragments/manticore/
COPY test.sh /home/fragments/test.sh

USER root

RUN chown -R fragments:fragments echidna
RUN chown -R fragments:fragments manticore

# Allow passwordless sudo for fragments
RUN echo 'fragments ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER fragments

CMD ["/bin/bash"]
