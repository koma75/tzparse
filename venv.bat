title xmltool
set HTTP_PROXY=http://localhost:8089
set HTTPS_PROXY=http://localhost:8089
if not exist .venv python -m venv .venv
cmd /k .venv\Scripts\activate.bat
