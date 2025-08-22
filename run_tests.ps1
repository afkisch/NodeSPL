# Run pytest with HTML report
pytest ./tests --html=./tests/report/report.html

# Ensure reports folder exists
if (!(Test-Path "./tests/report")){
    New-Item -ItemType Directory -Path "./tests/report"
}

if (!(Test-Path "./docs")){
    New-Item -ItemType Directory -Path "./docs"
}

# Move report to reports/latest.html (overwrite if exists)
Move-Item -Force .\tests\report\report.html .\docs\index.html

# Git commit only the report
git add docs\index.html
git commit -m "Update pytest report" 2>$null
git push origin main