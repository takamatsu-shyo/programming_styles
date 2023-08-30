cat your_file.txt | tr '[:upper:]' '[:lower:]' |\
    tr -d '.,' | tr -s ' ' '\n' | sort | \
    grep -v -w -f <(tr ',' '\n' < stopwords.txt) |\
    uniq -c | sort -nr | head -n 26

