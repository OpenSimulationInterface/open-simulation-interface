@ECHO OFF
SET Targetpath=..\.antora\modules\interface
SET Symlinkroot=..\..\..

mklink /D %Targetpath%\images %Symlinkroot%\doc\images

mklink /D %Targetpath%\pages %Symlinkroot%\doc

@REM mklink /D %Targetpath%\partials %Symlinkroot%\_additional_content

@REM mklink /D %Targetpath%\attachments %Symlinkroot%\_attachments

PAUSE