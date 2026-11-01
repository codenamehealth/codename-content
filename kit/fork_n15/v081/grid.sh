for P in "7.5 0.5 170" "6.0 0.8 160" "9.0 0.5 170" "6.0 0.5 150" "7.5 0.8 185"; do set -- $P
echo "P $1 $2 $3"; SA=$1 SB=$2 VB=$3 python3 r81.py stat 0 200 | grep -v "hook bottom"
done
echo GRIDDONE
