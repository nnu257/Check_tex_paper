# Check_tex_paper

## 概要
- &lt;日本語の>Tex形式の論文原稿における間違いをチェックします．   
- 論文投稿前に，校正の一環として使ってください．
- ルールベースの文字列マッチングをしているので，texの種類やversionに関係なく使えます．

## チェック対象
- 接続詞が連続していないか
- 修正すべき単語：「困難」「そして」など (再現率重視で抽出しています)
- 改行を妨げるチルダが適切な場所にあるか：図~\ref{hoge}など
- 半角・全角カンマの表記揺れ
- bibitemの表記揺れ：Vol, vol, num, Noなど

## 使用法
1. Texファイルをtxtに変換する  
   - 原稿をtex2txt.pyと同じディレクトリに置き，tex2txt.pyの変数input_fileを原稿のファイル名とする
   - python3 tex2txt.py  
2. 1で得たtxtファイルをtex_check.pyで処理し，出力を確認
   - python3 tex_check.py
4. 1で得たtxtファイルをEnnoなどの校正サイトも使って校正
  
*各プログラムの動作確認には，各々の原稿を利用してください．  
(本当は動作確認用の原稿を付けたかったのですが，私の原稿だと，学会の著作権が...)

## 処理内容の概要
txt2txt.py  
tex特有のコマンドの削除や，table, figureの削除などを行うことで，単純な文書ファイルに変換する．  
具体的には \documentclass, \par, \sectionなどを削除する．  
なお，refやbibitemは，削除していない．前者はチルダ記号の有無を，後者は構成をチェックするためである．  
  
tex_check.py  
変換されたtxtを受け取り，校正すべき点がないか確認する．  
確認はルールベースで行う．
