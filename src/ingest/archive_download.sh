#!/bin/bash

cd ~/Cloud_Bigdata_Analysis/github_data/raw

for year in 2021 2022 2023 2024 2025
do
    for month in {1..12}
    do
        for hour in {0..11}
        do
            file="${year}-$(printf "%02d" $month)-01-${hour}.json.gz"
            url="https://data.gharchive.org/${file}"

            if [ -f "$file" ]; then
                echo "skip $file"
            else
                wget "$url"
            fi
        done
    done
done
