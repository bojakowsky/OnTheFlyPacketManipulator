QT += core
QT += network
QT -= gui

CONFIG += c++11

TARGET = PacketAnalyzerTests
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    test.cpp

HEADERS += \
    test.h
