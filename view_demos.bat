@echo off
echo Opening Deal Finder Voice Agent Demo Files...
echo.

echo Opening Email Preview...
start "" "email_preview.html"
timeout /t 2 /nobreak >nul

echo Opening Call Logs...
start "" "call_logs.html"
timeout /t 2 /nobreak >nul

echo Opening Extracted Information...
start "" "extracted_info.html"
timeout /t 2 /nobreak >nul

echo.
echo All demo files have been opened in your default browser.
echo Press any key to exit...
pause >nul
