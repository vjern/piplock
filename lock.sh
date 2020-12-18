latest() {
    curl -L "https://pypi.org/pypi/$1/json" 2> /dev/null \
    | jq .releases \
    | jq -r keys \
    | tr -d '"\|,\|]\| ' \
    | grep '^[0-9.]\+$' \
    | sort -h \
    | tail -1
}

name() {
    echo "$1" | grep -Po '^[\w\[\]-]*'
}

file=$1
if [[ ! -f "$file" ]]; then
    echo "No such file: $file"
    exit 1
fi
echo 1>&2 file=$file

cat $file | while read line || [ -n "$line" ]; do
    if [[ `echo $line | grep -P '^\s*#'` ]] || [[ ! "`echo $line`" ]]; then
        echo $line
        continue
    fi
    name=$(name $line)
    if [[ $name != $line ]]; then
        echo $line
    else
        echo $name==$(latest $name)
    fi
done