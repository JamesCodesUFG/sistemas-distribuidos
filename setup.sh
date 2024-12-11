echo "Clonando o repositório..."

get clone https://github.com/JamesCodesUFG/sistemas-distribuidos.git

cd sistemas-distribuidos

echo "Instalando dependências..."

pip install -r requirements.txt

cd tarefa

exho "Executando o script node.py..."

python3 node.py