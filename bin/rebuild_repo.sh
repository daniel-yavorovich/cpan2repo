#!/bin/bash
BRANCH="$1"

cd /var/lib/repo
mkdir -p ./dists/$BRANCH/main
chmod -R 777 ./dists/$BRANCH

dpkg-scanpackages -m ./dists/$BRANCH/main/binary-amd64 /dev/null > ./dists/$BRANCH/main/binary-amd64/Packages
cat ./dists/$BRANCH/main/binary-amd64/Packages | gzip -9c > ./dists/$BRANCH/main/binary-amd64/Packages.gz

tee ./dists/$BRANCH/Release << EOF
Origin: example.com
Label: apt repository
Description: Private repo
Codename: $BRANCH
Poll: $BRANCH
Architecture: amd64 source
SignWith: yes
Components: main
MD5Sum:
EOF

md5sum=$(md5sum ./dists/$BRANCH/main/binary-amd64/Packages | cut -d ' ' -f1)
sizeinbytes=$(ls -l ./dists/$BRANCH/main/binary-amd64/Packages | cut -d ' ' -f5)
printf " "$md5sum" %16d main/binary-amd64/Packages\n" $sizeinbytes >> ./dists/$BRANCH/Release
printf " "$md5sum" %16d main/binary-i386/Packages\n" $sizeinbytes >> ./dists/$BRANCH/Release

md5sum=$(md5sum ./dists/$BRANCH/main/binary-amd64/Packages.gz | cut -d ' ' -f1)
sizeinbytes=$(ls -l ./dists/$BRANCH/main/binary-amd64/Packages | cut -d ' ' -f5)
printf " "$md5sum" %16d main/binary-amd64/Packages.gz\n" $sizeinbytes >> ./dists/$BRANCH/Release
printf " "$md5sum" %16d main/binary-i386/Packages.gz\n" $sizeinbytes >> ./dists/$BRANCH/Release

rm -f ./dists/$BRANCH/Release.gpg
gpg -bao ./dists/$BRANCH/Release.gpg ./dists/$BRANCH/Release