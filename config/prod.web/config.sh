#!/bin/bash

########################################################################
# reset root password
echo $1 | passwd --stdin

########################################################################
# add an admin user.  kbedwell to start.  Add him to the wheel group
adduser web
echo $2 | passwd web
usermod -a -G wheel web
adduser kbedwell
echo $1 | passwd --stdin kbedwell
usermod -a -G wheel kbedwell
usermod -a -G web kbedwell


