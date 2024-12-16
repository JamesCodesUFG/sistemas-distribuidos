
echo "Instalando dependências..."

pip install pika
pip install rpyc
pip install putil

echo "Clonando o repositório..."

git clone https://github.com/JamesCodesUFG/sistemas-distribuidos.git

cd sistemas-distribuidos/tarefas

cp -R ./utils ./remote/maestro

cd ./remote/maestro

echo "Executando o script maestro.py..."

python3 maestro.py $1
