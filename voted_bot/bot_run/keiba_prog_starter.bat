@echo off
mode 103,20
chcp 65001
cd %~dp0
cls

title = KEIBA POLL BOT MENU
color 03

echo #######################################################################################################
echo db   dD d88888b d888888b d8888b.  .d8b.    d8888b.  .d88b.  db      db        d8888b.  .d88b.  d888888b
echo 88 ,8P' 88'       `88'   88  `8D d8' `8b   88  `8D .8P  Y8. 88      88        88  `8D .8P  Y8. `~~88~~'
echo 88,8P   88ooooo    88    88oooY' 88ooo88   88oodD' 88    88 88      88        88oooY' 88    88    88
echo 88`8b   88~~~~~    88    88~~~b. 88~~~88   88~~~   88    88 88      88        88~~~b. 88    88    88
echo 88 `88. 88.       .88.   88   8D 88   88   88      `8b  d8' 88booo. 88booo.   88   8D `8b  d8'    88
echo YP   YD Y88888P Y888888P Y8888P' YP   YP   88       `Y88P'  Y88888P Y88888P   Y8888P'  `Y88P'     YP  
echo #######################################################################################################

echo １^:投票レースの取得

echo ２^:競馬投票ボットの起動（メインモード）

echo ３^:投票モードのみ起動

echo ４^:ゲームモードのみ起動

echo ５^:テストモード

echo ６^:プログラムの終了


echo #######################################################################################################




set answer=
set /p answer=＞＞

cd ../
echo %CD%

if %answer%==1 (
    echo レース取得プログラムを起動します
    cd keiba_race_getting_prog\getting_uma_info
) else if %answer%==2 (
    echo 競馬ボットを起動します（ ===MAIN MODE === ）
    cd keiba_vote_prog
) else if %answer%==3 (
    echo ボットを起動します（vote modeのみ）
    cd keiba_vote_prog
) else if %answer%==4 (
    echo ボットを起動します（game mode）
    cd keiba_vote_prog
) else if %answer%==5 (
    echo botテスト（test mode）
    cd keiba_vote_prog
) else if %answer%==6 (
    echo プログラムを終了します
) else (
    echo 不正な値です。プログラムを終了しますので再起動してください。
)



if %answer%==1 (
    timeout 3 /NOBREAK >nul
    echo レース取得プログラムを起動します...
    start "GETTING RACE PROG" py %CD%\keiba_race_scry.py
) else if %answer%==2 (
    timeout 3 /NOBREAK >nul
    echo botを起動します...
    start "DISCORD KEIBA BOT" py %CD%\voted_keiba.py --vote_mode True --game_mode True
) else if %answer%==3 (
    timeout 3 /NOBREAK >nul
    echo botを起動します...
    start "DISCORD KEIBA BOT" py %CD%\voted_keiba.py --vote_mode True
) else if %answer%==4 (
    timeout 3 /NOBREAK >nul
    echo botを起動します...
    start "DISCORD KEIBA BOT" py %CD%\voted_keiba.py --game_mode True
) else if %answer%==5 (
    timeout 3 /NOBREAK >nul
    echo botを起動します...
    start "DISCORD KEIBA BOT" py %CD%\voted_keiba.py --test_mode True
) else (
    echo 関知していない値の入力があります。
)



