import QtQuick
import QtQuick.Controls

Button {
    id: root

    property real uiScale: 1.0
    property bool accentChip: false
    hoverEnabled: true

    implicitHeight: Math.round(30 * uiScale)

    contentItem: Text {
        text: root.text
        color: root.accentChip ? "#1f3645" : "#4f6472"
        font.pixelSize: Math.max(10, Math.round(10 * uiScale))
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        radius: height / 2
        color: root.down ? "#e3edf6" : (root.hovered ? (root.accentChip ? "#eef6ff" : "#f6f8fa") : (root.accentChip ? "#edf5fd" : "#fbfcfd"))
        border.color: root.accentChip ? "#d3e3f2" : "#e4ebf1"
        opacity: root.enabled ? 1.0 : 0.5
    }
}
