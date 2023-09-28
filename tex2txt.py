import re

input_file = "ex_Tokai_1.tex"
output_file = input_file[:-4] + ".txt"

with open(input_file, "r") as f:
    txt = f.read()
    
# 前置きの削除
pattern = r".*\\begin{document}"
txt = re.sub(pattern, "", txt, flags=(re.DOTALL))

# begin-endの消去(table, figureなど，中身も消すもの)
patterns_be = ["table", "figure"]
for ele in patterns_be:
    pattern = r"\\begin{" + ele + r"}.*?\\end{" + ele + r"}"
    txt = re.sub(pattern, "", txt, flags=(re.DOTALL))

# 見出しの削除
# 見出しを書いて，改行せずに中身を書くことは想定していない
txt = re.sub(r"\\section.*", "", txt)
txt = re.sub(r"\\subsection.*", "", txt)
txt = re.sub(r"\\subsubsection.*", "", txt)

# begin-endの削除(itimizeなど，中身は消さないもの)
txt = re.sub(r"\\begin{.*}\n*", "", txt)
txt = re.sub(r"\\end{.*}\n*", "", txt)

# その他雑多なもの
txt = re.sub(r"\\par", "", txt)
txt = re.sub(r"\\maketitle", "", txt)
txt = re.sub(r"\\item", "", txt)
txt = re.sub(r"%.*", "", txt)
txt = re.sub(r"\\label.*", "", txt)
txt = re.sub(r"\\footnote{.*?}", "", txt)
txt = re.sub(r"\\footnotesize", "", txt)
txt = re.sub(r"\\vspace{.*?}", "", txt)

# \bibitemの最初に@@@bibitem@@@を追加
txt = re.sub(r"\\bibitem", r"@@@bibitem@@@\n\\bibitem", txt, 1)

# ref, cite, urlの中身を削除
txt = re.sub(r"\\ref{.*}", r"\\ref{hoge}", txt)
txt = re.sub(r"\\cite{.*}", r"\\cite{hoge}", txt)
txt = re.sub(r"\\url{.*}", r"\\url{hoge}", txt)

# 整形
txt = re.sub("\n{2,100000}", "\n\n", txt)
txt = txt.strip()


    
open(output_file, "w").write(txt)
