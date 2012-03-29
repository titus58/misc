#!/bin/bash

if [ ! -f cscope.files ];
then
    echo "Building cscope.files"
    find `pwd` -type f -name "*.h" >> cscope.files
    find `pwd` -type f -name "*.c" >> cscope.files
fi

rm cscope.out
cscope -b