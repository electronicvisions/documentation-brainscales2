#!/bin/bash

set -euo pipefail

FILENAME="index.html"

cat << EOF > $FILENAME
<!DOCTYPE html>
<title>BrainScales-2 Documentation Versions</title>
<html lang="en">
<body>
<h2>Select your desired version of the BrainScaleS-2 documentation</h2>

<p>
EBRAINS commonly defines a software release cycle.
Releases are versioned defining a unambiguous software state at each point in time.
As the research infrastructure is evolving further, there is an additional (roughly weekly) software snapshot called "EBRAINS_experimental_release".
This snapshot combines all the newest developments and newest features, but is more likely to have bugs regarding the interoperability of the EBRAINS software components.
To get the newest features, please use the "EBRAINS_experimental_release".
The BrainScaleS team supports hardware usage for the current stable release and the experimental state.
To reproduce results on older EBRAINS software states, please <a href="https://electronicvisions.github.io/hbp-sp9-guidebook/getting_help.html">contact us directly</a>.
The documentation is version-specific as it changes in lockstep with the software state.
Please choose the documentation matching your software release.
</p>
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
