#!/bin/bash
# script to run the extraction of features for all midi files in my_data/Brahms
for filename in my_data/Brahms/*.mid; do
    python3 features/extracting_features.py "$filename"
done