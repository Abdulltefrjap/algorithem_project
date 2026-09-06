@echo off
chcp 65001 >nul
title مشروع الخوارزميات - تشغيل
color 0A

echo ============================================
echo   نظام ادارة المهام - مشروع الخوارزميات
echo ============================================
echo.

cd /d "%~dp0"

:: ─── Backend ─────────────────────────────────
echo [1/4] تثبيت متطلبات Backend...
cd backend
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [خطأ] فشل تثبيت متطلبات Backend
    pause
    exit /b 1
)

echo [2/4] تجهيز البيانات التجريبية...
python seed_data.py
echo.

:: ─── Frontend ────────────────────────────────
echo [3/4] تثبيت متطلبات Frontend...
cd ..\frontend
if not exist "node_modules\" (
    call npm install
) else (
    echo       node_modules موجود - تخطي التثبيت
)
echo.

:: ─── تشغيل السيرفرات ─────────────────────────
echo [4/4] تشغيل السيرفرات...
cd ..

start "Backend - FastAPI" cmd /k "cd /d "%~dp0backend" && echo Backend: http://localhost:8000/docs && uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

start "Frontend - React" cmd /k "cd /d "%~dp0frontend" && echo Frontend: http://localhost:5173 && npm run dev"

timeout /t 5 /nobreak >nul

start http://localhost:5173

echo.
echo ============================================
echo   تم التشغيل بنجاح!
echo ============================================
echo   Backend:  http://localhost:8000/docs
echo   Frontend: http://localhost:5173
echo.
echo   تسجيل الدخول:
echo   المستخدم: ahmed
echo   كلمة المرور: 123456
echo ============================================
echo.
echo اضغط اي زر لاغلاق هذه النافذة...
echo (السيرفرات ستبقى تعمل في نوافذ منفصلة)
pause >nul
