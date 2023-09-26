# Check_tex_paper

## 概要
&lt;日本語の>Tex形式の論文原稿における間違いをチェックします．  
論文投稿前に，校正の一環として使ってください．

## チェック対象
- 接続詞のチェック：「そして」など
- 連続する接続詞のチェック(未実装)
- 他機能も追加予定

## 使用法
1. Texファイルをtxtに変換する  
   tex2txt.pyと同じディレクトリに置き，tex2txt.pyのinput_fileにファイル名を入れる  
2. 1で得たtxtファイルをtex_check.pyでも同様に処理し，出力を確認  
3. 1で得たtxtファイルをEnnoなどの校正サイトで校正  
