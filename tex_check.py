import re

# ファイル名
input_file = "ex_NLC_1.txt"
output_file = input_file[:-4:] + "_errors.txt"

# 読み込み
lines = open(input_file, "r").readlines()

# チェック対象と，エラーを保持するリスト．[行数，種類]を要素とする．
# 修正すべき文字列
change_words = ["難しい", "困難","不十分", "そして", "これは","加えて","なぜなら，","よって", "および", "なのである", "ただし", "つまり", "このため","これにより","これらにより", "この結果", "及び","せた", "故に","を行う","を行った","行な", "依って","である，", "。", "、", "(U|u)ndergraduate",  "(", "結果として", "先述","次に述べる","のは", "具体的には", "分の一", "ためだと", "読み取れる", "か検証する", "を見ると","を確認すると","ていった"]
change = []
# チルダまわり
tilda_words = ["手法\d", "\ref{.*}節", "(表|図)\ref{.*}", r"ら\\cite"]
tilda = []
# 半角カンマ
comma = []
# 手法1~3みたいなやつ
num_omit = []
# bibitem
before_bibitem = True
bibitem = []

# 1行ずつ処理
for i, line in enumerate(lines):
    
    # bibitem前なら
    if before_bibitem:          
        # エラーチェック    
        # 修正すべき文字列の確認
        for j, word in enumerate(change_words):
            if word in line:
                change.append([i+1, j+1])
    
        # 手法，節，表，図の前後のチルダの確認
        for j, word in enumerate(tilda_words):
            # 本来ならば1行で複数マッチすることもあるが，校正では何回もチェック(実行)するはずなので，1つだけキャッチする
            if re.search(word, line):
                tilda.append([i+1, j+1])
                
        # 半角カンマ
        if re.search(", ", line):
            comma.append(i+1)
            
        # 手法1~3みたいな
        if re.search("(\d~\d)|(\d，\d)|(\d-\d)", line):
            num_omit.append(i+1)
    
    # bibitem後なら
    else: 
        # 最後は全角カンマで終わっているか
        if not re.search("(.*})|(^\d{4}．)|(参照．)|(.*，)|(^$)", line):
            bibitem.append([i+1, 1])
        
        # Vol, No, ppがある場合，小文字・大文字が統一されているか
        if re.search("(vol)|(no)|(Num)|(num)|(PP)|(Pp)", line):
            bibitem.append([i+1, 2])
            
        # Vol, No, ppがある場合，チルダ，ピリオドの挿入がされているか
        if re.search("(Vol)|(No)|(pp)", line):
            if ("~" not in line) or ("." not in line):
                bibitem.append([i+1, 3])
                
    # bibitem用フラグ
    if "@@@bibitem@@@" in line:
        before_bibitem = False
        
# 連続する接続詞のチェック
tmp_conjunction = ""
conjunction = []
# 対象とする接続詞のリスト
conjunctions = ["そのため", "例えば", "具体的には", "よって", "ゆえに", "次に", "それにより", "以上のことから", "このように", "その結果", "しかしながら", "なぜならば", "ところが", "また", "さらに", "いっぽう", "反対に", "この理由は", "なお", "すなわち", "しかし"]

# 一行ごとにチェックしていき，マッチすればtmpに入れる
# 同じものが連続したらアウト
# 空白行でリセットする
for i, line in enumerate(lines):
    for j, word in enumerate(conjunctions):
        if word in lines:
            if word == tmp_conjunction:
                conjunction.append([i+1, j+1])
            tmp_conjunction = word
            
# 出力
with open(output_file, "w") as f:
    f.write("校正対象案の一覧\n")
    num_all = len(change + tilda + conjunction + comma + num_omit + bibitem)
    f.write(f"件数：{num_all}件\n\n")
    f.write("＜修正すべき?文字列＞\n")
    for error in change:
        f.write(f"{error[0]}行目：{change_words[error[1]-1]}\n")
    if not change:
        f.write("該当事項はありません．\n")
        
    f.write("\n＜改行を防ぐチルダ記号の欠如＞\n")
    for error in tilda:
        if error[1] == 1:
            word = "手法"
        elif error[1] == 2:
            word = "節"
        elif error[1] == 3:
            word = "表or図"
        else:
            word = "cite"
            
        f.write(f"{error[0]}行目：{word}\n")
    if not tilda:
        f.write("該当事項はありません．\n")


    f.write("\n＜接続詞の連続＞\n")
    for error in conjunction:
        f.write(f"{error[0]}行目：{conjunctions[error[1]-1]}が連続？")
    if not conjunction:
        f.write("該当事項はありません．\n")
        
    f.write("\n＜半角カンマ+スペースは全角カンマに＞\n")
    for error in comma:
        f.write(f"{error}行目\n")
    if not comma:
        f.write("該当事項はありません．\n")
        
    f.write("\n＜手法1~3とかは手法1~手法3に直す，-ではなく~を使う＞\n")
    for error in num_omit:
        f.write(f"{error}行目\n")
    if not num_omit:
        f.write("該当事項はありません．\n")
        
    f.write("\n＜bibitem関連の校正＞\n")
    for error in bibitem:
        if error[1] == 1:
            advice = "全角カンマの使用を推奨"
        elif error[1] == 2:
            advice = "Vol, No, pp, 大文字/小文字に注意"
        else:
            advice = "チルダとピリオドの挿入を推奨 例：Vol.~3"
            
        f.write(f"{error[0]}行目：{advice}\n")
    if not bibitem:
        f.write("該当事項はありません．\n")
        
    f.write("\n\n＜他に確認すべきこと＞\n")
    f.write("参考文献の書き方は，自分が提出する学会の論文誌のものを参考にしたか?\n")
    f.write("変数は$hoge$のように囲んだか？\n")
    f.write("論文中の単語は表記を統一したか？  例：モデル-手法，初期データ-最初に与えるデータ\n")
    f.write("手段を書くときは，「~~で」ではなく，「~~により」と記述したか？\n")
    f.write("「具体的には」とある後には，具体的な情報が記述されているか？\n")
    f.write("表は，必要なところは幅が均等になっていて，見出しは中央揃え，文字は左揃え，数字は右揃えにしたか？\n")
    f.write("「2つ」などの数字は漢数字にしたか？\n")