echo "Instalando dependências..."

pip install pika
pip install rpyc
pip install putil

echo "Clonando o repositório..."

git clone https://github.com/JamesCodesUFG/sistemas-distribuidos.git

cd sistemas-distribuidos/tarefas

cp -R ./utils ./remote/node

cd ./remote/node

echo "Executando o script node.py..."

python3 node.py
