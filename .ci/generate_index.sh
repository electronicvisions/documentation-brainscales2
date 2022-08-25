#!/bin/bash

set -euo pipefail

FILENAME="index.html"

cat << EOF > $FILENAME
<!DOCTYPE html>
<title>BrainScales 2 Documentation Versions</title>
<html lang="en">
<body>
<h1>Select your desired version of the BrainScaleS 2 documentation</h1>
EOF

echo '<ul>' >> $FILENAME
for ev in */; do
    echo '   <li><a href="'$ev'">'$ev'</a></li>' >> $FILENAME
done
echo '</ul>' >> $FILENAME

cat << EOF >> $FILENAME
</body>
</html>
EOF
