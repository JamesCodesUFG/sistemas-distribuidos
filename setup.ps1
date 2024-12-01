# Variáveis de configuração
$repoUrl = "https://github.com/JamesCodesUFG/sistemas-distribuidos"     # URL do repositório do GitHub
$localDir = 'C:\_temp\teste'                                            # Diretório onde será clonado o repositório                                           # Nome do arquivo zip (se aplicável)
$pythonScript = "t.py"                                                  # Nome do script Python para executar

# 1. Clonar o repositório do GitHub
Write-Host "Clonando o repositorio do GitHub..." -ForegroundColor Green

if (!(Test-Path -Path $localDir)) {
    git clone $repoUrl $localDir
} else {
    Write-Host "O diretório já existe. Pulando o clone..." -ForegroundColor Yellow
}

# 2. Entrar no diretório do repositório
Set-Location -Path $localDir

# 4. Executar o script Python
Write-Host "Executando o script Python..." -ForegroundColor Green
python $pythonScript

# 5. Exibir mensagem de finalização
Write-Host "Processo concluido!" -ForegroundColor Cyan