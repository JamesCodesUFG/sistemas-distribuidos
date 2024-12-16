echo "Instalando dependências..."

pip install pika
pip install rpyc
pip install putil

echo "Clonando o repositório..."

git clone https://github.com/JamesCodesUFG/sistemas-distribuidos.git

cd sistemas-distribuidos/tarefas

cp -R ./utils ./remote/client

cd ./remote/client

echo "Executando o script client.py..."

python3 client.py $1
