#!/bin/sh

set -e

rm -f system

( cd input-generators/syspy ; ./$2 ; mv system ../.. ; cd ../.. )

# ( rsh -. $1 ./h  $3    ) < /dev/null 2>&1 | tee /dev/null
# ( rsh -. $1 ./pd $3 $4 ) < /dev/null 2>&1 | tee /dev/null

( ./h  $3    ) < /dev/null 2>&1 | tee /dev/null
( ./pd $3 $4 ) < /dev/null 2>&1 | tee /dev/null
