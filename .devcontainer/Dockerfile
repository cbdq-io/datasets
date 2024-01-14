FROM ghcr.io/cbdq-io/flyte:latest

ENV PATH /usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/code/.local/bin
USER root

RUN apt-get clean \
  && apt-get update \
  && apt-get install --yes \
    libsnappy-dev \
    sudo \
    zsh \
  && useradd --home-dir /home/code --create-home --groups sudo --shell /usr/bin/zsh code

COPY sudoers /etc/sudoers

USER code

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
