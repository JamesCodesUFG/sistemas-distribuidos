#include "servidorop.h"
#define sendbufferlen 1024

typedef struct addr {
    char rua[128];
    char nRua;
    char bairro[128];
    char nBairro;
    int numero;
} addr;

typedef struct db {
    char banco[128];
    char nBanco;
    char agencia[128];
    char nAgencia;
    char conta[128];
    int nConta;
} db;

typedef struct data {
    char nome[128];
    char nNome;
    addr endereco;
    db dadosBancarios;
} data;



data databuffer[1024];
int bufflen = 0;

void printData(data p) {
    printf("n: %s:%d\n", p.nome, p.nNome);
    printf("e:\n\t%s:%d\n\t%s:%d\n\t%d\n", p.endereco.rua, p.endereco.nRua, p.endereco.bairro, p.endereco.nBairro, p.endereco.numero);
    printf("b:\n\t%s:%d\n\t%s:%d\n\t%s:%d\n", p.dadosBancarios.banco, p.dadosBancarios.nBanco, p.dadosBancarios.agencia, p.dadosBancarios.nAgencia, p.dadosBancarios.conta, p.dadosBancarios.nConta);
    printf("t: %d\n", p.nNome + p.endereco.nBairro + p.endereco.nRua + 4 + p.dadosBancarios.nAgencia + p.dadosBancarios.nBanco + p.dadosBancarios.nConta);
}


void insertData(char in[DEFAULT_BUFLEN]) {
    data new;
    char flag = 0;
    int c = 0;
    if (bufflen == 1024) return;

    flag = in[c++];
    for (int i = 0; i < flag; i++) new.nome[i] = in[c++];
    new.nome[flag] = '\0';
    new.nNome = flag;

    flag = in[c++];
    for (int i = 0; i < flag; i++) new.endereco.rua[i] = in[c++];
    new.endereco.rua[flag] = '\0';
    new.endereco.nRua = flag;
    
    flag = in[c++];
    for (int i = 0; i < flag; i++) new.endereco.bairro[i] = in[c++];
    new.endereco.bairro[flag] = '\0';
    new.endereco.nBairro = flag;

    flag = in[c++];
    for (int i = 0; i < 4; i++) ((char*) &(new.endereco.numero))[i] = in[c++];
    
    flag = in[c++];
    for (int i = 0; i < flag; i++) new.dadosBancarios.banco[i] = in[c++];
    new.dadosBancarios.banco[flag] = '\0';
    new.dadosBancarios.nBanco = flag;

    flag = in[c++];
    for (int i = 0; i < flag; i++) new.dadosBancarios.agencia[i] = in[c++];
    new.dadosBancarios.agencia[flag] = '\0';
    new.dadosBancarios.nAgencia = flag;

    flag = in[c++];
    for (int i = 0; i < flag; i++) new.dadosBancarios.conta[i] = in[c++];
    new.dadosBancarios.conta[flag] = '\0';
    new.dadosBancarios.nConta = flag;

    databuffer[bufflen++] = new;
}

int addToBuffer(SOCKET Client, char in[DEFAULT_BUFLEN], int len) {
    int iResult = recv(Client, in, len, 0);
    printf("Wawa\n");
    if (iResult == 0) return 0;
    else if (iResult > 0) {
        insertData(in);
        printf("bufflen: %d\n", bufflen);
        printData(databuffer[bufflen-1]);
        return 0;
    } 
    printf("recv failed with error: %d\n", WSAGetLastError());
    return 1;
}

int sendMessage(SOCKET Client, char datasender[4096], int *c, int force) {
    if (*c <= sendbufferlen & !force) return 0; 
    
    if (!ISTEST) {
        printf("\n%d, %d\n", bufflen, *c);
        for (int i = 0; i < *c; i++) {
            printf("%03d:%02x:%c\n", i, (unsigned char) datasender[i], datasender[i]);
        }
        printf("\n");
        //*c = 0;
        //return 0;
    }


    int iSendResult = send(Client, datasender, *c, 0);
    *c = 0;
    if (iSendResult == SOCKET_ERROR) {
        printf("send failed with error: %d\n", WSAGetLastError());
        closesocket(Client);
        WSACleanup();
        return -1;
    }
    printf("Bytes sent: %d\n", iSendResult);
    return 1;
}

int sendBuffer(SOCKET Client, char in[DEFAULT_BUFLEN]) {
    unsigned char datasender[sendbufferlen];
    int c = 0;
    data d;
    printf("Wawawa\n");
    
    /*/
    int iSendResult = send(Client, "Hello World!", 12, 0);

    return 0;

    //*/
    for (int i = 0; i < bufflen; i++) {
        printf("%d\n", i);
        d = databuffer[i];

        datasender[c++] = d.nNome;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; d.nome[j]; j++) {
            datasender[c++] = d.nome[j];
            sendMessage(Client, datasender, &c, 0);
        }

        datasender[c++] = d.endereco.nRua;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; d.endereco.rua[j]; j++) {
            datasender[c++] = d.endereco.rua[j];
            sendMessage(Client, datasender, &c, 0);
        }
        
        datasender[c++] = d.endereco.nBairro;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; d.endereco.bairro[j]; j++) {
            datasender[c++] = d.endereco.bairro[j];
            sendMessage(Client, datasender, &c, 0);
        }
        datasender[c++] = 0x80;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; j < 4; j++) { 
            datasender[c++] = ((unsigned char*) &d.endereco.numero)[j];
            sendMessage(Client, datasender, &c, 0);
        }

        datasender[c++] = d.dadosBancarios.nBanco;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; d.dadosBancarios.banco[j]; j++) {
            datasender[c++] = d.dadosBancarios.banco[j];
            sendMessage(Client, datasender, &c, 0);
        }

        datasender[c++] = d.dadosBancarios.nAgencia;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; d.dadosBancarios.agencia[j]; j++) {
            datasender[c++] = d.dadosBancarios.agencia[j];
            sendMessage(Client, datasender, &c, 0);
        }

        datasender[c++] = d.dadosBancarios.nConta;
        sendMessage(Client, datasender, &c, 0);
        for (int j = 0; d.dadosBancarios.conta[j]; j++) {
            datasender[c++] = d.dadosBancarios.conta[j];
            sendMessage(Client, datasender, &c, 0);
        }
        
    }
    sendMessage(Client, datasender, &c, 1);
    return 0;
}

int getDataStream(SOCKET Client, char in[DEFAULT_BUFLEN], int len) {
    printf("%c\n", in[0]);
    if (in[0] == 'P') return addToBuffer(Client, in, len);
    else if (in[0] == 'G') return sendBuffer(Client, in);
    else return -1;
}

int testRecieve() {
    char testbuf[] = {
        0x05, 'V', 'i', 't', 'o', 'r',
        0x04, '2', '8', '-', 'A',
        0x0D, 'S', 't', '.', ' ', 'A', 'e', 'r', 'o', 'p', 'o', 'r', 't', 'o',
        0x80, 0x27, 0x01, 0x00, 0x00,
        0x02, 'B', 'B',
        0x03, '3', '2', '1',
        0x04, '1', '3', '4', '0', 0x00
        };
    char testbuf2[] = {
        0x1E, 'T', 'i', 'a', 'g', 'o', ' ', 'G', 'o', 'n', 'c', 'a', 'l', 'v', 'e', 's', ' ', 'M', 'a', 'i', 'a', ' ', 'G', 'e', 'r', 'a', 'l', 'd', 'i', 'n', 'e',
        0x07, 'R', 'u', 'a', ' ', 'R', '1', '6', 
        0x0D, 'V', 'i', 'l', 'a', ' ', 'I', 't', 'a', 't', 'i', 'a', 'i', 'a',
        0xff, 0x07, 0x00, 0x00, 0x00,
        0x0f, 'B', 'a', 'n', 'c', 'o', ' ', 'd', 'o', ' ', 'B', 'r', 'a', 's', 'i', 'l',
        0x07, '0', '9', '-', '8', '9', '7', '6',
        0x05, '5', '4', '3', '2', '6' 
    };
    for (int i = 0; i < 50; i++) {
        insertData(testbuf);
        insertData(testbuf2);
    }
}

int testSend() {
    SOCKET empty;
    testRecieve();
    sendBuffer(empty, NULL);
}