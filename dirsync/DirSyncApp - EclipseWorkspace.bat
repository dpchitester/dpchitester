@echo on
setlocal enabledelayedexpansion
cd \Projects\DirSyncApp

set src=%FLASH0%
set dst=%TEMP%

set rd=Projects\EclipseWorkspace

set arg1=%src%\%rd%
set arg2=%dst%\%rd%
set args=%arg1% %arg2%

dirsync_libs.bat !args!

