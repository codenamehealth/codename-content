for P in "1.1 1.0" "1.2 0.8" "1.0 0.9" "1.3 1.0"; do set -- $P
echo "P $1 $2"; SPK=$1 CAP=$2 python3 r85.py search 0 600
done; echo GDONE
