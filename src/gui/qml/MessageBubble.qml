import QtQuick
import QtQuick.Layouts

Item {
    id: root

    property string role: "assistant"
    property string sender: "System"
    property string text: ""
    property string timestamp: ""
    property string tone: "reply"
    property bool compact: false
    property bool groupedWithPrevious: false
    property bool groupedWithNext: false
    property real uiScale: 1.0
    property int availableWidth: 640

    readonly property bool fromUser: role === "user"
    readonly property bool isSystem: tone === "system" || role === "system"
    readonly property bool isEvent: tone === "event"
    readonly property bool isError: tone === "error"
    readonly property bool isReply: !fromUser && !isSystem && !isEvent && !isError
    readonly property int paddingX: Math.round((fromUser ? 14 : 16) * uiScale)
    readonly property int paddingTop: Math.round(9 * uiScale)
    readonly property int paddingBottom: Math.round(7 * uiScale)
    readonly property int minimumBubbleWidth: Math.round((compact ? 160 : 185) * uiScale)
    readonly property int maximumBubbleWidth: Math.round((availableWidth - Math.round(18 * uiScale)) * (compact ? 0.78 : 0.62))
    readonly property int timeReserveWidth: Math.round(48 * uiScale)
    readonly property int contentWidth: Math.max(textBlock.implicitWidth, timeReserveWidth)
    readonly property real topLeftRadius: Math.round((isSystem ? 14 : (fromUser ? 18 : (groupedWithPrevious ? 8 : 18))) * uiScale)
    readonly property real topRightRadius: Math.round((isSystem ? 14 : (fromUser ? (groupedWithPrevious ? 8 : 18) : 18)) * uiScale)
    readonly property real bottomLeftRadius: Math.round((isSystem ? 14 : (fromUser ? 18 : (groupedWithNext ? 8 : 18))) * uiScale)
    readonly property real bottomRightRadius: Math.round((isSystem ? 14 : (fromUser ? (groupedWithNext ? 8 : 18) : 18)) * uiScale)

    width: availableWidth
    implicitHeight: card.implicitHeight + Math.round((groupedWithNext ? 1 : 4) * uiScale)

    Rectangle {
        id: card
        width: isSystem ? Math.min(parent.width, Math.round(520 * uiScale)) :
               Math.max(minimumBubbleWidth, Math.min(maximumBubbleWidth, contentWidth + root.paddingX * 2))
        implicitHeight: contentColumn.implicitHeight + root.paddingTop + root.paddingBottom
        anchors.horizontalCenter: isSystem ? parent.horizontalCenter : undefined
        anchors.left: fromUser || isSystem ? undefined : parent.left
        anchors.right: fromUser ? parent.right : undefined
        color: isError ? "#fff1f2" :
               isSystem ? "#d2dfeb" :
               isEvent ? "#eef5fb" :
               fromUser ? "#d9fdd3" : "#ffffff"
        border.color: isError ? "#f3c0c8" :
                      isSystem ? "#c7d5e1" :
                      isEvent ? "#d5e1ec" :
                      fromUser ? "#b9e4b2" : "#dce4ea"
        border.width: isSystem || isEvent || isError ? 1 : (fromUser ? 0 : 1)
        topLeftRadius: root.topLeftRadius
        topRightRadius: root.topRightRadius
        bottomLeftRadius: root.bottomLeftRadius
        bottomRightRadius: root.bottomRightRadius
        clip: true

        Column {
            id: contentColumn
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: root.paddingX
            anchors.rightMargin: root.paddingX
            anchors.topMargin: root.paddingTop
            spacing: Math.round((groupedWithPrevious ? 2 : 4) * uiScale)

            RowLayout {
                visible: (isSystem || isEvent || isError) && !groupedWithPrevious
                width: parent.width
                spacing: Math.round(10 * uiScale)

                Text {
                    text: isEvent ? "EVENT" : (isSystem ? "SYSTEM" : sender)
                    color: isError ? "#a24a58" : "#6f8798"
                    font.pixelSize: Math.max(9, Math.round(10 * uiScale))
                    font.letterSpacing: 2
                }

                Item {
                    Layout.fillWidth: true
                }

                Text {
                    visible: timestamp.length > 0
                    text: timestamp
                    color: "#8a9aa8"
                    font.pixelSize: Math.max(10, Math.round(10 * uiScale))
                }
            }

            Text {
                id: textBlock
                width: card.width - contentColumn.anchors.leftMargin - contentColumn.anchors.rightMargin
                text: root.text
                wrapMode: Text.Wrap
                color: isError ? "#8f3040" : "#243744"
                font.pixelSize: Math.max(14, Math.round(15 * uiScale))
                font.bold: isEvent
                lineHeight: 1.24
                topPadding: 0
                bottomPadding: 0
            }

            RowLayout {
                visible: !isSystem
                width: parent.width
                spacing: Math.round(4 * uiScale)

                Item {
                    Layout.fillWidth: true
                }

                Text {
                    text: timestamp
                    color: fromUser ? "#6d8970" : "#8a9aa8"
                    font.pixelSize: Math.max(9, Math.round(10 * uiScale))
                    rightPadding: 1
                }
            }
        }
    }
}
