#!/bin/bash

exec sudo docker run -it --device=/dev/video0 --device=/dev/vchiq -v /opt/vc:/opt/vc 546150905175.dkr.ecr.us-west-2.amazonaws.com/kinesis-video-producer-sdk-cpp-raspberry-pi /bin/sh -c "gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480 ! omxh264enc control-rate=2 target-bitrate=512000 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,profile=baseline ! kvssink stream-name="plantly-pp1" access-key="" secret-key="" aws-region="""
