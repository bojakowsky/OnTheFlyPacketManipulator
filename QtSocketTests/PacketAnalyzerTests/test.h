#ifndef TEST_H
#define TEST_H

#include <QObject>
#include <QTextStream>
#include <QString>
#include <QTcpSocket>
#include <QUdpSocket>
class Test : public QObject
{
    Q_OBJECT
public:
    explicit Test(QObject *parent = 0);
    ~Test();

    QTcpSocket *socket = 0;
    QUdpSocket *udpSocket = 0;
    QUdpSocket *udpSocketSender = 0;
signals:

public slots:
    void connected();
    void disconnected();
    void printData();
    void printUDPData();
};

#endif // TEST_H
