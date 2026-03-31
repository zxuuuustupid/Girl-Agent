import QtQuick

Rectangle {
    id: root

    property string text: ""
    property real uiScale: 1.0

    implicitWidth: label.implicitWidth + Math.round(20 * uiScale)
    implicitHeight: Math.round(24 * uiScale)
    radius: implicitHeight / 2
    color: "#d4e3ef"
    border.color: "#c8d8e4"

    Text {
        id: label
        anchors.centerIn: parent
        text: root.text
        color: "#5d7487"
        font.pixelSize: Math.max(10, Math.round(10 * uiScale))
    }
}
