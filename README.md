### Sistemas Distribuidos
Esse repositório é destinado para armazenamento e controle de versionamento das atividades realizadas ao longo da disciplina Sistemas Distribuidos 2024/2. 

### Ativar RabbitMq
É necessário iniciar o RabbitMq e passar o ip da maquina para todos os clientes do RabbitMq.

> docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management

### Ativar RPyC Registry

Windows:
> python c:\users\tiago\appdata\local\programs\python\python312\scripts\rpyc_registry.exe -l true

Ubuntu:
> rpyc_registry.py -l true

### Setup
Ubuntu:
> chmod +x setup.sh
> setup.sh

### Requirements

> pip install pika
> pip install rpyc
> pip install psutil