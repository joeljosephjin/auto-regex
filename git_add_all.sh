mv data/truth_uploaded.csv data/truth_uploaded_NEW.csv
cp data/truth.csv data/truth_uploaded.csv
git add .
rm data/truth_uploaded.csv
mv data/truth_uploaded_NEW.csv data/truth_uploaded.csv
