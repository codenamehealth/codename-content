for P in "620 2.6" "560 2.6" "680 3.0" "520 2.2"; do set -- $P
echo "IMP $1 FRIC $2"; IMP=$1 FRIC=$2 python3 r89.py search 0 400
done; echo GRIDDONE
