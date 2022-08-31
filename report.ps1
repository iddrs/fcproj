$opt = '&Sim', '&Não'

# Processando o código Python
$RunR = $Host.UI.PromptForChoice('Executar Python', 'Deseja gerar os dados?', $opt, 0)
if ($RunR -eq 0) {
    python main.py
} else {
    Write-Host 'Pulando a geração dos dados com Python...'
}

# Lendo o nome do arquivo de destino
$OutputFile = Get-Content -Path cache\arquivo.txt
$Output = Join-Path -Path 'output' -ChildPath $OutputFile

# Gerando a saída em PDF
pdflatex -file-line-error -halt-on-error -output-directory cache/ -output-format pdf report.tex
# Executa duas vezes por causa do longtable
pdflatex -file-line-error -halt-on-error -output-directory cache/ -output-format pdf report.tex

# Renomeando a saída para output
Move-Item -Path cache\report.pdf -Destination $Output -Force

# Removendo lixo
$ClearTrash = $Host.UI.PromptForChoice('Limpando lixo', 'Deseja limpar arquivos de cache?', $opt, 0)
if ($ClearTrash -eq 0) {
    Remove-Item -Path cache/*.*
    Remove-Item -Path output/*.aux
    Remove-Item -Path output/*.log
    Remove-Item -Path output/*.toc
} else {
    Write-Host 'Os arquivos de cache não foram apagados...'
}
