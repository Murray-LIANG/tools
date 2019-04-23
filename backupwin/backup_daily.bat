@echo off
set from="C:\Users\liangr"
set to="E:\Ryan\backup_win"
echo Backup from %from% to %to%
echo Copying corp.
xcopy %from%\corp %to%\corp /e/i/d/h/r/y
echo Copying Documents.
xcopy %from%\Documents %to%\Documents /e/i/d/h/r/y
echo Copying ebooks.
xcopy %from%\ebooks %to%\ebooks /e/i/d/h/r/y
echo Copying git.
xcopy %from%\git %to%\git /e/i/d/h/r/y
echo Copying Pictures.
xcopy %from%\Pictures %to%\Pictures /e/i/d/h/r/y
echo Copying tools.
xcopy %from%\tools %to%\tools /e/i/d/h/r/y
exit
