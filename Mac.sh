#!/bin/bash
TPATH=$(find . -type f -name "GUIMAC.py")
BPATH=$(find . -type f -name "sub_cmd.py")
python3 $TPATH & python3 $BPATH



