#!/bin/bash
KEY=`git annex lookupkey $1`
URL='http://conceptnet-api-1.media.mit.edu/downloads/annex/vector-ensemble/'
echo -n "$1 $URL"
git annex examinekey $KEY --format '${hashdirlower}${key}/${key}\n'
