@echo off

echo [+] STARTING DOWNLOADING!

REM Download the tar files
for /l %%n in (0,1,19) do (
    echo [+] DOWNLOADING scener_%%n.tar...
    curl -L -O https://github.com/imangali01/scener-dataset/releases/download/v2.0/scener_%%n.tar
)

echo [+] COMPLEATED DOWNLOADING!
echo [+] STARTING UNPACKING!

REM Extract the tar files
for /l %%n in (0,1,19) do (
    echo [+] UNPACKING scener_%%n.tar...
    tar -zxf scener_%%n.tar
)

echo [+] COMPLEATED!
pause
