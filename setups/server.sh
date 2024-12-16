echo "Instalando dependências..."

pip install pika
pip install rpyc
pip install putil

echo "Clonando o repositório..."

git clone https://github.com/JamesCodesUFG/sistemas-distribuidos.git

cd sistemas-distribuidos/tarefas

cp -R ./utils ./remote/server

cd ./remote/server

echo "Executando o script server.py..."

python3 server.py $1
