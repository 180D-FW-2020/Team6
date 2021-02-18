#!/bin/bash
APATH=$(find . -type f -name "vid_gui_client_latest_user1.py")
BPATH=$(find . -type f -name "imu_sub.py")
CPATH=$(find . -type f -name "chatcli.py")
TPATH=$(find . -type f -name "sample.py")
python3 $TPATH & python3 $APATH & python3 $BPATH & python3 $CPATH



