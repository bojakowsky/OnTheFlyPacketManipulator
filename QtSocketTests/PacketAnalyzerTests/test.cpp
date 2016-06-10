#include "test.h"

Test::Test(QObject *parent) : QObject(parent)
{
    socket = new QTcpSocket();
    connect(socket, SIGNAL(connected()), this, SLOT(connected()));
    connect(socket, SIGNAL(disconnected()), this, SLOT(disconnected()));
    connect(socket, SIGNAL(readyRead()), this, SLOT(printData()));

    socket->connectToHost("192.168.0.101", 1000);
    socket->waitForConnected(45000);
    if (socket->state() == QTcpSocket::ConnectedState){
        socket->write("ALOHA MAN");
    }


    udpSocket = new QUdpSocket();
    connect(udpSocket, SIGNAL(readyRead()), this, SLOT(printUDPData()));

    QHostAddress address("192.168.0.100");
    udpSocket->bind(address, 1000);

    udpSocketSender = new QUdpSocket();
    udpSocketSender->writeDatagram("Jeden dwa trzy!", QHostAddress("192.168.0.101"), 999);


}

void Test::printUDPData()
{
    QByteArray datagram;
    do {
            datagram.resize(udpSocket->pendingDatagramSize());
            udpSocket->readDatagram(datagram.data(), datagram.size());
            qDebug(datagram.data());
            udpSocketSender->writeDatagram("Uno dos tres!", QHostAddress("192.168.0.101"), 999);
        } while (udpSocket->hasPendingDatagrams());


}

void Test::printData()
{
    QString data = socket->readAll();
    qDebug(data.toStdString().c_str());
}

Test::~Test()
{
    if (socket != 0)
        delete socket;

    if (udpSocket != 0)
        delete udpSocket;
}

void Test::connected()
{
    qDebug("connected");
}

void Test::disconnected()
{
    qDebug("disconnect");
}
