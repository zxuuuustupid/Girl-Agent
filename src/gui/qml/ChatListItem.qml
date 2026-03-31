import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: root

    property string title: ""
    property string subtitle: ""
    property string timeLabel: ""
    property bool active: false
    property string badgeText: ""
    property real uiScale: 1.0
    property url avatarSource: ""
    readonly property int sideInset: Math.round(10 * uiScale)
    hoverEnabled: true
    clip: true

    implicitHeight: Math.round(64 * uiScale)
    padding: 0

    contentItem: RowLayout {
        anchors.fill: parent
        anchors.leftMargin: root.sideInset
        anchors.rightMargin: root.sideInset
        spacing: Math.round(10 * root.uiScale)

        Rectangle {
            width: Math.round(42 * root.uiScale)
            height: width
            radius: width / 2
            color: root.active ? "#5ca7eb" : "#d7dee5"
            border.color: "transparent"
            clip: true

            Image {
                anchors.fill: parent
                anchors.margins: 2
                source: root.avatarSource
                fillMode: Image.PreserveAspectCrop
                smooth: true
                clip: true
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 0
            Layout.alignment: Qt.AlignVCenter

            RowLayout {
                Layout.fillWidth: true
                spacing: Math.round(8 * root.uiScale)

                Text {
                    text: root.title
                    color: root.active ? "white" : "#1f2f3d"
                    font.pixelSize: Math.max(13, Math.round(13 * root.uiScale))
                    font.weight: Font.DemiBold
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                    maximumLineCount: 1
                }

                Text {
                    text: root.timeLabel
                    color: root.active ? "#d9ecff" : "#8a9aa8"
                    font.pixelSize: Math.max(9, Math.round(10 * root.uiScale))
                    Layout.alignment: Qt.AlignTop
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: Math.round(8 * root.uiScale)

                Text {
                    text: root.subtitle
                    color: root.active ? "#eef7ff" : "#708291"
                    font.pixelSize: Math.max(10, Math.round(11 * root.uiScale))
                    elide: Text.ElideRight
                    Layout.fillWidth: true
                    maximumLineCount: 1
                }

                Rectangle {
                    visible: root.badgeText !== ""
                    width: Math.max(Math.round(18 * root.uiScale), badgeLabel.implicitWidth + Math.round(10 * root.uiScale))
                    height: Math.round(18 * root.uiScale)
                    radius: height / 2
                    color: root.active ? "#ffffff" : "#5ca7eb"

                    Text {
                        id: badgeLabel
                        anchors.centerIn: parent
                        text: root.badgeText
                        color: root.active ? "#3f8fd9" : "white"
                        font.pixelSize: Math.max(10, Math.round(11 * root.uiScale))
                    }
                }
            }
        }
    }

    background: Rectangle {
        radius: Math.round(10 * root.uiScale)
        color: root.active ? "#5ca7eb" : (root.down ? "#eef2f5" : (root.hovered ? "#f3f6f9" : "transparent"))
        border.width: root.active ? 0 : 1
        border.color: root.hovered ? "#e4ebf0" : "transparent"
        clip: true
    }
}
