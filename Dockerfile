#
# frc_rekt dockerfile
# Gets dependencies installed and cached for fast building.
# Intended to be used for cicd, not general purpose.
#
# https://github.com/jaustinpage/frc_rekt
#

FROM alpine:latest

# credit to https://github.com/drillan/docker-alpine-scipy/blob/master/Dockerfile
# credit to https://github.com/amancevice/pandas/blob/master/0.19/python3/Dockerfile
# credit to https://github.com/rui/docker-matplotlib/blob/master/Dockerfile

RUN apk update \
&& apk add \
    aspell \
    aspell-en \
    ca-certificates \
    enchant \
    freetype \
    libmagic \
    libpng \
    libstdc++ \
    libgfortran \
    python3 \
&& apk add --no-cache --virtual=build_dependencies \
    build-base \
    freetype-dev \
    gcc \
    gfortran \
    g++ \
    libpng-dev \
    make \
    python3-dev \
&& ln -s /usr/include/locale.h /usr/include/xlocale.h \
&& mkdir -p /tmp/build \
&& cd /tmp/build/ \
&& wget http://www.netlib.org/blas/blas-3.6.0.tgz \
&& wget http://www.netlib.org/lapack/lapack-3.6.1.tgz \
&& tar xzf blas-3.6.0.tgz \
&& tar xzf lapack-3.6.1.tgz \
&& cd /tmp/build/BLAS-3.6.0/ \
&& gfortran -O3 -std=legacy -m64 -fno-second-underscore -fPIC -c *.f \
&& ar r libfblas.a *.o \
&& ranlib libfblas.a \
&& mv libfblas.a /tmp/build/. \
&& cd /tmp/build/lapack-3.6.1/ \
&& sed -e "s/frecursive/fPIC/g" -e "s/ \.\.\// /g" -e "s/^CBLASLIB/\#CBLASLIB/g" make.inc.example > make.inc \
&& make lapacklib \
&& make clean \
&& mv liblapack.a /tmp/build/. \
&& cd / \
&& export BLAS=/tmp/build/libfblas.a \
&& export LAPACK=/tmp/build/liblapack.a \
&& python3 -m pip --no-cache-dir install pip -U \
&& python3 -m pip --no-cache-dir install \
    cython \
    matplotlib \
    numpy \
    pandas \
    pycodestyle \
    pydocstyle \
    pyenchant \
    pylint \
    pytest \
    pytest-cov \
    python-magic \
    requests \
    scipy \
    seaborn \
    sphinx \
    yapf \
&& apk del --purge -r build_dependencies \
&& rm -rf /tmp/build
