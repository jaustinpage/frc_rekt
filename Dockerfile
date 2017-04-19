#
# frc_rekt dockerfile
# Gets dependencies installed and cached for fast building.
# Intended to be used for cicd, not general purpose.
#
# https://github.com/jaustinpage/frc_rekt
#

FROM ubuntu

# Get our dependencies file
COPY scripts/dependencies /tmp/dependencies

# Run dependencies
RUN /tmp/dependencies

WORKDIR /root/

# Used to expire the layer if master has changed
ADD https://api.github.com/repos/jaustinpage/frc_rekt/compare/master...HEAD /dev/null
# We are cloning the git repo to speed up build time. NOTE: Must update from branch if testing code
RUN git clone https://github.com/jaustinpage/frc_rekt /app/frc_rekt

# Switch working directory to git repo
WORKDIR /app/frc_rekt

# Note: Anything below this should be populating cached data, and should be "redone"
# at test time. The only reason for doing this ahead of time is to speed up building and testing
# A good rule: if it aint in .gitignore, you dont want it in the docker container
# Note 2: Don't rely on the github repo when running scripts, because when building in a branch,
# master file paths are not guarenteed. Instead, copy what you need.

# Download the python dependencies and populate our ./env virtualenv
COPY scripts/py-dependencies /tmp/py-dependencies
RUN /tmp/py-dependencies

# Copy the curves, to prevent excessive downloads from motors.vex.com
COPY data/vex data/vex/

# Download the curves, this should no-op, but just in case
COPY scripts/download_curves /tmp/download_curves
RUN /tmp/download_curves

CMD ["bash"]
