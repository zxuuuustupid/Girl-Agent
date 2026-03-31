import QtQuick
import QtQuick.Controls

Button {
    id: root

    property real uiScale: 1.0
    property string symbol: "?"
    property bool accent: false
    hoverEnabled: true

    implicitWidth: Math.round(30 * uiScale)
    implicitHeight: implicitWidth
    padding: 0

    contentItem: Text {
        text: root.symbol
        color: root.accent ? "white" : "#6c7f8e"
        font.pixelSize: Math.max(10, Math.round(11 * root.uiScale))
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        opacity: root.enabled ? 1.0 : 0.55
    }

    background: Rectangle {
        radius: width / 2
        color: root.accent ? (root.down ? "#4e97de" : (root.hovered ? "#5ea8f0" : "#5ca7eb"))
                           : (root.down ? "#eef2f5" : (root.hovered ? "#f4f7fa" : "transparent"))
        border.width: root.accent ? 0 : 1
        border.color: root.hovered ? "#e3eaf0" : "transparent"
        opacity: root.enabled ? 1.0 : 0.8
    }
}
