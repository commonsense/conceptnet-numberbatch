#!/bin/bash
KEY=`git annex lookupkey $1`
BASE='http://conceptnet-api-1.media.mit.edu/downloads/annex/vector-ensemble'
LOCATION=`git annex examinekey $KEY --format '${hashdirlower}${key}/${key}'`
git annex addurl --file $1 $BASE/$LOCATION
