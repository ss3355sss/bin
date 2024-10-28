@echo off

set ENGINE=%1
set ENGINE_DIR=%2

if "%ENGINE%" == "" (
    echo "Failed to get %%ENGINE%%"
    exit \b 0
)

if "%ENGINE_DIR%" == "" (
    echo "Failed to get %%ENGINE_DIR%%"
    exit \b 0
)

reg query "HKEY_CURRENT_USER\Software\Epic Games\Unreal Engine\Builds" /v %ENGINE% 2>nul
if %errorlevel% equ 0 (
    echo "Remove Registry Key : { %ENGINE%, %ENGINE_DIR% }"
    reg delete "HKEY_CURRENT_USER\Software\Epic Games\Unreal Engine\Builds" /v %ENGINE% /f
) else (
    echo "Add Registry Key : { %ENGINE%, %ENGINE_DIR% }"
    reg add "HKEY_CURRENT_USER\Software\Epic Games\Unreal Engine\Builds" /v %ENGINE% /t REG_SZ /d %ENGINE_DIR% 
)
