import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root

    property string title: ""
    property string value: ""
    property real uiScale: 1.0

    radius: Math.round(12 * uiScale)
    color: "#ffffff"
    border.color: "#e1e8ee"
    implicitHeight: Math.max(56, Math.round(62 * uiScale))

    Column {
        anchors.fill: parent
        anchors.margins: Math.round(10 * uiScale)
        spacing: Math.round(3 * uiScale)

        Text {
            text: root.title
            color: "#7c8b98"
            font.pixelSize: Math.max(9, Math.round(10 * uiScale))
            font.letterSpacing: 1
        }

        Text {
            text: root.value
            color: "#243744"
            font.pixelSize: Math.max(13, Math.round(14 * uiScale))
            wrapMode: Text.Wrap
        }
    }
}
