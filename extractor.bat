@echo off
for /L %%i in (0,1,9) do (
    @echo Extracting scener_%%i.tar...
    tar -zxf scener_%%i.tar
)