git switch paqs-website
git pull
python3 get_publications.py
git commit -m "Updated publications $(date)" publications.html
git push
git checkout master
git merge paqs-website -m "updated publications"
