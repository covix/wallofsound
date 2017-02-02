#!/bin/zsh
#
#   Copyright 2016 Nur Hussein (hussein@unixcat.org)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

WALLDIR=${HOME}/.musicwall

mkdir -p $WALLDIR

if [[ ${1:0:4} == "http" ]] ; then 
	WALLFILE=$WALLDIR/$(basename "$1")
	if [ -e $WALLFILE ]; then
		rm -f $WALLFILE
	fi
	
	cd $WALLDIR
	wget -q $1
elif [[ $1 == /* ]] ; then
	WALLFILE=$WALLFILE
else
	WALLFILE="/Users/covix/Pictures/20150108_151605.jpg"
fi

echo $WALLFILE > $WALLDIR/WALLURI

