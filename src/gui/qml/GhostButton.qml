import QtQuick
import QtQuick.Controls

Button {
    id: root

    property real scaleRef: 1.0
    hoverEnabled: true

    implicitHeight: Math.round(38 * scaleRef)
    implicitWidth: Math.round(92 * scaleRef)

    contentItem: Text {
        text: root.text
        color: "#385266"
        font.pixelSize: Math.max(11, Math.round(12 * root.scaleRef))
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        radius: Math.round(10 * root.scaleRef)
        color: root.down ? "#e9eef3" : (root.hovered ? "#f4f7fa" : "#ffffff")
        border.color: "#d6e0e8"
    }
}
