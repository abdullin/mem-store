#!/bin/bash
# install this python script the hacky way
set -ex

TARGET=/usr/local/bin/mem
DIR=$(pwd)


cat <<EOF > $TARGET
#!/bin/bash
$DIR/venv/bin/python $DIR/mem.py $@
EOF

chmod +x $TARGET
