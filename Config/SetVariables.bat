@echo off

:argument-branch
if "%1"=="" (
	::-------------------------------------- Get P4V Workspace Name 
	for %%a in (%cd%) do (for %%b in ("%%~dpa\.") do set "Parent=%%~nxb" )
	set PROJECT_NAME=%Parent%

	goto :main

)else (
	set PROJECT_NAME=%1
	goto :main
)

:get-absolute:
	set abspath=%~f1
	goto :eof

:main
	::-------------------------------------- Get Current Directory
	for %%i in (.) do set CurDir=%%~nxi
	set GAME_NAME=%CurDir%

	::set Workspace Dir
	call :get-absolute %cd%\..\..
	set WORKSPACE_DIR=%abspath%

	::set Configuration Dir
	set DATA_DIR=%WORKSPACE_DIR%\Data
	set GAME_DIR=%WORKSPACE_DIR%\Program\%GAME_NAME%
	set GAME_BINARY_DIR=%GAME_DIR%\Binaries\Win64

	set ENGINE_DIR=%WORKSPACE_DIR%\Program\UnrealEngine\Engine
	set ENGINE_BINARY_DIR=%ENGINE_DIR%\Binaries\Win64

	::set Batch
	set BUILD_BAT=%ENGINE_DIR%\Build\BatchFiles\Build.bat
	set RUNUAT_BAT=%ENGINE_DIR%\Build\BatchFiles\RunUAT.bat

	::set Executable
	set GAME_EXECUTABLE=%GAME_BINARY_DIR%\%GAME_NAME%.exe
	set UE4EDITOR_EXECUTABLE=%ENGINE_BINARY_DIR%\UE4Editor-cmd.exe


	echo.
	echo #------------------------- %GAME_NAME% Configuration
	echo %WORKSPACE_DIR%
	echo %DATA_DIR%
	echo %GAME_DIR%
	echo %ENGINE_DIR%

	if not exist %DATA_DIR% 	( echo Failed to get valid DATA_DIR & exit /b 1 )
	if not exist %GAME_DIR% 	( echo Failed to get valid GAME_DIR & exit /b 1 )
	if not exist %ENGINE_DIR% 	( echo Failed to get valid ENGINE_DIR & exit /b 1 )

	exit /b 0

