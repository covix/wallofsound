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

# Requires https://github.com/hnarayanan/shpotify
command -v spotify >/dev/null 2>&1 || { echo "I require spotify but it's not installed.  Aborting." >&2; exit 1; }

# while : ; do
#         mpc idle &>/dev/null
#         # the sed will exclude things between parenthesis like (feat. Pit Bull)
#         SONG="$(mpc current | grep -v "player|mixer")"
#         ./wallofsound.py $SONG 2>/dev/null
# done

INFO=""
while : ; do
    INFO_NEW=`spotify info | head -n3 | tail -n2 | cut -d':' -f 2 | sed -e 's/^[ ]*//' | cut -d'-' -f1`

    if [ "$INFO" != "$INFO_NEW" ]
    then
        INFO=$INFO_NEW

        ARTIST=`echo $INFO | head -n1`
        SONG=`echo $INFO | tail -n1 `

        ARG="$ARTIST - $SONG"
        echo $ARG
        python wallofsound.py $ARG  # 2>/dev/null
        echo
    fi

    sleep 10
done
