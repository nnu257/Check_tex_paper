# Check_tex_paper

## 概要
- &lt;日本語の>Tex形式の論文原稿における間違いをチェックします．   
- 論文投稿前に，校正の一環として使ってください．

## チェック対象
- 接続詞のチェック：「そして」など
- 連続する接続詞のチェック(未実装)
- 他機能も追加予定

## 使用法
1. Texファイルをtxtに変換する  
   - 原稿をtex2txt.pyと同じディレクトリに置き，tex2txt.pyの変数input_fileを原稿のファイル名とする  
2. 1で得たtxtファイルをtex_check.pyでも同様に処理し，出力を確認  
3. 1で得たtxtファイルをEnnoなどの校正サイトも使って校正
  
*tex2txt.pyの動作確認には，demo.texを利用してください．  
*tex_check.pyの動作確認には，各々の原稿を利用してください．(私の原稿だと，学会の著作権が...)

## 処理内容の概要
txt2txt.py  
tex特有のコマンドの削除や，table, figureの削除などを行うことで，単純な文書ファイルに変換する．  
具体的には \documentclass, \par, \sectionなどを削除する．  
なお，refやbibitemは，削除していない．前者はチルダ記号の有無を，後者は構成をチェックするためである．  
  
tex_check.py  
変換されたtxtを受け取り，校正すべき点がないか確認する．  
確認はルールベースで行う．
