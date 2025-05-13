@echo off
echo.
echo Lancement des tests avec generation du rapport HTML...
python -m pytest TEST/test_api.py --html=TEST/test_api-report.html
pause

