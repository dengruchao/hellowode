git add --all .
set /p msg=please input commit message:
git commit -m "%msg%"
git push sae master:1
