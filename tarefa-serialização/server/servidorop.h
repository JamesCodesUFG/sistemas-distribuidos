#ifndef Trolib_ServidorOP
#define Trolib_ServidorOP
#undef UNICODE

#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0601
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <stdio.h>
#pragma comment (lib, "Ws2_32.lib")
// #pragma comment (lib, "Mswsock.lib")
#define DEFAULT_BUFLEN 4096
#define DEFAULT_PORT "27015"
#define ISTEST 0
int getDataStream(SOCKET Client, char in[DEFAULT_BUFLEN], int len);
int testRecieve();
int testSend();
#endif