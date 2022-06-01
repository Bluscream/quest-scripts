@echo off
if "%~1"=="" (
    setlocal
    set "yourDir=G:\Steam\steamapps\common\Beat Saber\Beat Saber_Data\CustomLevels"
    set "yourExt=*"
    pushd %yourDir%
    for %%x in (%yourExt%) do (
        adb push "%%~x" "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/%%~nx"
        echo adb push "%%~x" "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/%%~nx"
    )
    popd
    endlocal
) else (
    for %%x in (%*) do (
        adb push "%%~x" "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/%%~nx"
        echo adb push "%%~x" "/sdcard/ModData/com.beatgames.beatsaber/Mods/SongLoader/CustomLevels/%%~nx"
    )
)
pause