#include <QCoreApplication>
#include <QObject>
#include "test.h"
int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    Test *test = new Test();
    return a.exec();
}



