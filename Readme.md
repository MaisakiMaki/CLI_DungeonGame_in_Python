copy right
このゲームの著作権は制作者のりまきに帰属するものとします。

# 使用上の注意
このゲームは専修大学鳳祭2025で公開したゲームとなっております。
著作権等は個人的にはあまり気にしませんが、あまり綺麗なコードではないため、
再配布に関してはご遠慮いただきたいと思います。
また、自作発言に関しても、あんまやってもメリットはないと思うのでやめた方がいいと思います。
今後、どこかのタイミングで有料になるかもしれませんが、ほとんどそんなことはないと思います。

# ゲームをプレイする前の注意点
このゲームは音声ファイルをゲーム上で操作するために
"playsound"と"pygame"をインストールしています
そのため、皆様各自のpcのコンソール上で
pip install playsound
pip install pygame
をしてもらい、インポートできる環境にしていただく必要があります。

また、このゲームは鳳祭で展示した際に幾つかの音声ファイルが入った
"assets"フォルダを用意していましたが、音声ファイルの再配布禁止等の観点から
今回の"rogueLike.zip"にassetsフォルダは含まれていません。
そのため、申し訳ございませんが、皆様各自でダウンロード音声ファイルをダウンロードしていただいて
assetsフォルダに入れるということを行っていただかないと音声が出ません。

一応音声なしでもプレイはできるのですが、ログの方に音声ファイルにアクセスができないと
表示されてしまう都合上、ダウンロードしていただくことをお勧めいたします。
以下が音声ファイルの名前とダウンロードした音声ファイルのurlとなります。

音声ファイル = {
    name: blind.mp3, url: https://otologic.jp/free/se/flashback01.html (回想5)
    name: clear.mp3, url: https://dova-s.jp/bgm/play6839.html (バグの関係上流れません)
    name: confuse.mp3, url: https://otologic.jp/free/se/dizzy01.html (めまい1)
    name: dungeon.mp3, url: https://peritune.com/blog/2020/04/24/dungeon_tower/ (Retoro loop)
    name: enemy_attack.mp3, url: https://www.springin.org/sound-stock/subcategory/attack/ (打撃1)
    name: equip.mp3 url: https://soundeffect-lab.info/sound/battle/ (刀を鞘にしまう1)
    name: fire.mp3, url: https://dova-s.jp/se/play378.html (Track1)
    name: hung.mp3, url: https://on-jin.com/sound/listshow.php?pagename=hito&title=%E8%85%B9%E3%81%AE%E8%99%AB05&janl=%E4%BA%BA%E9%96%93%E7%B3%BB%E9%9F%B3&bunr=%E8%85%B9%E3%81%AE%E8%99%AB&kate=%E4%BD%93%E3%83%BB%E8%83%B8%E3%83%BB%E8%85%B9
    name: Itemget.mp3, url: https://dova-s.jp/se/play640.html
    name: level.wav, url: https://commons.nicovideo.jp/works/nc219832
    name: paralysis.mp3, url: https://otologic.jp/free/se/electric-shock01.html (電撃2)
    name: player_attack.mp3, url: https://www.springin.org/sound-stock/subcategory/attack/ (斬撃4)
    name: rotten1.mp3, url: https://commons.nicovideo.jp/works/nc280152
    name: poison.mp3, url: http://www.kurage-kosho.info/mp3/poison01.mp3
    name: rotten2.mp3, url: https://commons.nicovideo.jp/works/nc257696
    name: rotten3.mp3, url: https://commons.nicovideo.jp/works/nc271511
    name: shot_gun.mp3, url: https://umipla.com/soundeffect/2703
    name: stair.wav, url: https://commons.nicovideo.jp/works/nc143371
    name: strong_poison.mp3, url: http://www.kurage-kosho.info/mp3/poison02.mp3
    name: use_item.mp3, url: https://commons.nicovideo.jp/works/nc78521
}

これらをダウンロードできたら
zipファイルを解凍したフォルダをカレントディレクトリとして
python3 main.py
とコンソール上で叩くとできると思います。

何かあれば
twitterの@NorimakiNetInfo
までよろしくお願いします。