sed -e 's/ 1:/:R1:/g' -e 's/ 2:/:R2:/g' -e 's/:R1\S*/:R1/g' -e 's/:R2\S*/:R2/g'  $1
