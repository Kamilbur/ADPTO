#!/usr/bin/bash
for filename in $(ls graph/ -I '*.sol')
do
    echo -n graph/$filename" "
done
