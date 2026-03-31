import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: Math.min(1280, Math.round(Screen.desktopAvailableWidth * 0.82))
    height: Math.min(820, Math.round(Screen.desktopAvailableHeight * 0.84))
    minimumWidth: 980
    minimumHeight: 660
    visible: true
    property var bridgeObj: bridge
    title: bridgeObj ? bridgeObj.agentName : "GirlAgent"
    color: "#dfe7ef"

    property real uiScale: Math.max(0.8, Math.min(width / 1520, height / 920))
    property int outerMargin: Math.round(18 * uiScale)
    property int sectionRadius: Math.round(14 * uiScale)
    property int sidebarWidth: compactMode ? Math.max(248, Math.round(width * 0.255)) : Math.max(286, Math.round(width * 0.22))
    property int drawerWidth: Math.max(232, Math.round(width * 0.185))
    property bool compactMode: width < 1360
    property bool infoDrawerOpen: false
    property bool composerHasText: composer.text.trim().length > 0

    ListModel {
        id: messageModel
    }

    function nowLabel() {
        return Qt.formatTime(new Date(), "hh:mm")
    }

    function appendMessage(role, text, tone) {
        messageModel.append({
            "role": role,
            "text": text,
            "tone": tone,
            "time": nowLabel()
        })
        messageView.positionViewAtEnd()
    }

    function isGrouped(index) {
        if (index <= 0 || index >= messageModel.count) {
            return false
        }
        const current = messageModel.get(index)
        const previous = messageModel.get(index - 1)
        if (!current || !previous) {
            return false
        }
        if (current.tone === "date" || previous.tone === "date") {
            return false
        }
        return current.role === previous.role && current.tone === previous.tone
    }

    function sendComposer() {
        const value = composer.text.trim()
        if (!value || bridge.busy) {
            return
        }
        bridge.sendMessage(value)
        composer.clear()
    }

    function applySuggestion(value) {
        composer.text = value
        composer.forceActiveFocus()
        composer.cursorPosition = composer.length
    }

    Component.onCompleted: {
        appendMessage("system", "Today", "date")
        appendMessage("assistant", "Say it. I am here.", "intro")
    }

    onCompactModeChanged: if (!compactMode) infoDrawerOpen = false

    Connections {
        target: bridge

        function onMessageAdded(role, text, tone) {
            appendMessage(role, text, tone)
        }

        function onErrorRaised(message) {
            appendMessage("system", message, "error")
        }

        function onConfirmationRequested(title, message, confirmLabel, cancelLabel) {
            confirmationTitle.text = title
            confirmationMessage.text = message
            confirmButton.text = confirmLabel
            cancelButton.text = cancelLabel
            confirmationDialog.open()
        }

        function onNumberRequested(title, message, defaultValue, minimumValue) {
            numberTitle.text = title
            numberMessage.text = message
            numberField.text = defaultValue.toString()
            numberDialog.minimum = minimumValue
            numberDialog.open()
        }
    }

    Rectangle {
        anchors.fill: parent
        color: "#dfe7ef"
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: outerMargin
        spacing: Math.round(10 * uiScale)

        Rectangle {
            Layout.preferredWidth: sidebarWidth
            Layout.fillHeight: true
            radius: sectionRadius
            color: "#ffffff"
            border.color: "#d7e0e7"

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.round(56 * uiScale)
                    color: "#5b96d1"
                    topLeftRadius: sectionRadius
                    topRightRadius: sectionRadius

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: Math.round(16 * uiScale)
                        anchors.rightMargin: Math.round(16 * uiScale)
                        spacing: Math.round(10 * uiScale)

                        CircleIconButton {
                            uiScale: window.uiScale
                            symbol: "\u2630"
                        }

                        Text {
                            text: "Chats"
                            color: "white"
                            font.pixelSize: Math.max(17, Math.round(18 * uiScale))
                            font.weight: Font.DemiBold
                        }

                        Item { Layout.fillWidth: true }

                        CircleIconButton {
                            uiScale: window.uiScale
                            symbol: infoDrawerOpen ? "\u2715" : "\u22EE"
                            onClicked: infoDrawerOpen = !infoDrawerOpen
                        }
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    anchors.leftMargin: Math.round(10 * uiScale)
                    anchors.rightMargin: Math.round(10 * uiScale)
                    anchors.topMargin: Math.round(10 * uiScale)
                    anchors.bottomMargin: Math.round(10 * uiScale)
                    spacing: Math.round(8 * uiScale)

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Math.round(34 * uiScale)
                        radius: Math.round(8 * uiScale)
                        color: "#f8fafc"
                        border.color: "#f0f4f7"

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: Math.round(12 * uiScale)
                            anchors.rightMargin: Math.round(12 * uiScale)
                            spacing: Math.round(8 * uiScale)

                            Text {
                                text: "\u2315"
                                color: "#9aacb9"
                                font.pixelSize: Math.max(10, Math.round(11 * uiScale))
                            }

                            Text {
                                text: "Search"
                                color: "#93a2af"
                                font.pixelSize: Math.max(11, Math.round(11 * uiScale))
                            }

                            Item { Layout.fillWidth: true }

                            Text {
                                text: "Ctrl+K"
                                color: "#93a2af"
                                font.pixelSize: Math.max(9, Math.round(10 * uiScale))
                            }
                        }
                    }

                    ChatListItem {
                        Layout.fillWidth: true
                        uiScale: window.uiScale
                        title: bridgeObj ? bridgeObj.agentName : "GirlAgent"
                        subtitle: bridgeObj && bridgeObj.busy ? "typing..." : (bridgeObj ? bridgeObj.statusLine : "")
                        timeLabel: nowLabel()
                        active: true
                        badgeText: bridgeObj && bridgeObj.busy ? "1" : ""
                        avatarSource: bridgeObj ? bridgeObj.heroImage : ""
                        onClicked: composer.forceActiveFocus()
                    }

                    Column {
                        Layout.fillWidth: true
                        spacing: Math.round(1 * uiScale)

                        Text {
                            text: "Suggested"
                            color: "#8392a0"
                            font.pixelSize: Math.max(10, Math.round(10 * uiScale))
                            leftPadding: Math.round(4 * uiScale)
                        }

                        Flow {
                            width: parent.width
                            spacing: Math.round(4 * uiScale)

                            SuggestionChip { uiScale: window.uiScale; text: "Stay"; onClicked: applySuggestion("Stay with me for a while.") }
                            SuggestionChip { uiScale: window.uiScale; text: "How are you?"; accentChip: true; onClicked: applySuggestion("How are you feeling today?") }
                            SuggestionChip { uiScale: window.uiScale; text: "Tell me"; onClicked: applySuggestion("Stop being cold and tell me the truth.") }
                        }
                    }

                    Item { Layout.fillHeight: true }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Math.round(46 * uiScale)
                        radius: Math.round(8 * uiScale)
                        color: "#f8fafc"
                        border.color: "#edf2f6"

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: Math.round(10 * uiScale)
                            anchors.rightMargin: Math.round(10 * uiScale)
                            spacing: Math.round(8 * uiScale)

                            Rectangle {
                                width: Math.round(28 * uiScale)
                                height: width
                                radius: width / 2
                                color: "#dce7f1"

                                Text {
                                    anchors.centerIn: parent
                                    text: bridgeObj ? bridgeObj.agentName.charAt(0) : "G"
                                    color: "#487fb6"
                                    font.pixelSize: Math.max(11, Math.round(12 * uiScale))
                                    font.weight: Font.DemiBold
                                }
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 0

                                Text {
                                    text: "Recent activity"
                                    color: "#8392a0"
                                    font.pixelSize: Math.max(9, Math.round(10 * uiScale))
                                }

                                Text {
                                    Layout.fillWidth: true
                                    text: bridgeObj ? bridgeObj.recentEvent : ""
                                    color: "#243744"
                                    elide: Text.ElideRight
                                    font.pixelSize: Math.max(11, Math.round(12 * uiScale))
                                }
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: sectionRadius
            color: "#e5ebf1"
            border.color: "#d6dee5"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: Math.round(10 * uiScale)
                spacing: Math.round(8 * uiScale)

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.round(54 * uiScale)
                    radius: Math.round(8 * uiScale)
                    color: "#ffffff"
                    border.color: "#dbe3e9"

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: Math.round(14 * uiScale)
                        anchors.rightMargin: Math.round(14 * uiScale)
                        spacing: Math.round(10 * uiScale)

                        Rectangle {
                            width: Math.round(38 * uiScale)
                            height: width
                            radius: width / 2
                            color: "#eef3f7"
                            border.color: "#dde5ec"

                            Image {
                                anchors.fill: parent
                                anchors.margins: 2
                                source: bridgeObj ? bridgeObj.heroImage : ""
                                fillMode: Image.PreserveAspectCrop
                                smooth: true
                                clip: true
                            }
                        }

                        ColumnLayout {
                            Layout.alignment: Qt.AlignVCenter
                            spacing: 2

                            RowLayout {
                                spacing: Math.round(6 * uiScale)

                                Text {
                                    text: bridgeObj ? bridgeObj.agentName : "GirlAgent"
                                    color: "#243744"
                                    font.pixelSize: Math.max(16, Math.round(17 * uiScale))
                                    font.weight: Font.DemiBold
                                }

                                Rectangle {
                                    width: Math.round(8 * uiScale)
                                    height: width
                                    radius: width / 2
                                    color: bridgeObj && bridgeObj.busy ? "#61c554" : "#93a2af"
                                }
                            }

                            Text {
                                text: bridgeObj && bridgeObj.busy ? "typing..." : (bridgeObj ? bridgeObj.subtitle : "")
                                color: "#7a8a97"
                                font.pixelSize: Math.max(10, Math.round(11 * uiScale))
                            }
                        }

                        Item {
                            Layout.fillWidth: true
                        }

                        CircleIconButton {
                            uiScale: window.uiScale
                            symbol: "\u22EE"
                            onClicked: infoDrawerOpen = !infoDrawerOpen
                        }

                        CircleIconButton {
                            uiScale: window.uiScale
                            symbol: "\u21BB"
                            onClicked: {
                                messageModel.clear()
                                appendMessage("system", "Today", "date")
                                bridge.resetConversation()
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 1
                    color: "#edf2f6"
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    radius: Math.round(10 * uiScale)
                    color: "#d9e5ef"
                    border.color: "#cfdae4"

                    Rectangle {
                        anchors.fill: parent
                        anchors.margins: 8
                        radius: Math.round(8 * uiScale)
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#dfe8ef" }
                            GradientStop { position: 0.55; color: "#dbe5ee" }
                            GradientStop { position: 1.0; color: "#d6e2ec" }
                        }
                        opacity: 0.98
                    }

                    Rectangle {
                        anchors.fill: parent
                        anchors.margins: 8
                        radius: Math.round(8 * uiScale)
                        color: "transparent"
                        opacity: 0.15

                        Column {
                            anchors.fill: parent
                            anchors.leftMargin: Math.round(26 * uiScale)
                            anchors.rightMargin: Math.round(26 * uiScale)
                            anchors.topMargin: Math.round(18 * uiScale)
                            spacing: Math.round(52 * uiScale)

                            Repeater {
                                model: 12
                                delegate: Rectangle {
                                    width: parent.width
                                    height: 1
                                    radius: 1
                                    color: "#ffffff"
                                }
                            }
                        }
                    }

                    ListView {
                        id: messageView
                        anchors.fill: parent
                        anchors.leftMargin: Math.round(12 * uiScale)
                        anchors.rightMargin: Math.round(16 * uiScale)
                        anchors.topMargin: Math.round(10 * uiScale)
                        anchors.bottomMargin: Math.round(8 * uiScale)
                        spacing: Math.round(4 * uiScale)
                        clip: true
                        model: messageModel
                        boundsBehavior: Flickable.StopAtBounds

                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AsNeeded
                            width: Math.round(6 * uiScale)
                            contentItem: Rectangle {
                                implicitWidth: Math.round(6 * uiScale)
                                radius: width / 2
                                color: parent.pressed ? "#8ea7bd" : "#a7bacb"
                                opacity: 0.9
                            }
                            background: Item {}
                        }

                        delegate: Loader {
                            width: messageView.width
                            property string roleData: model.role
                            property string textData: model.text
                            property string toneData: model.tone
                            property string timeData: model.time
                            property bool groupedPrevious: window.isGrouped(index)
                            property bool groupedNext: index < messageModel.count - 1 && (function() {
                                const current = messageModel.get(index)
                                const next = messageModel.get(index + 1)
                                if (!current || !next) {
                                    return false
                                }
                                if (current.tone === "date" || next.tone === "date") {
                                    return false
                                }
                                return current.role === next.role && current.tone === next.tone
                            })()
                            sourceComponent: toneData === "date" ? dateChipDelegate : messageDelegate
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Math.round(60 * uiScale)
                    radius: Math.round(8 * uiScale)
                    color: "#ffffff"
                    border.color: "#dbe3e9"

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: Math.round(8 * uiScale)
                        anchors.rightMargin: Math.round(8 * uiScale)
                        anchors.topMargin: Math.round(6 * uiScale)
                        anchors.bottomMargin: Math.round(6 * uiScale)
                        spacing: Math.round(8 * uiScale)

                        TextArea {
                            id: composer
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            color: "#243744"
                            placeholderText: "Write a message..."
                            placeholderTextColor: "#93a2af"
                            wrapMode: TextEdit.Wrap
                            selectByMouse: true
                            font.pixelSize: Math.max(14, Math.round(15 * uiScale))
                            topPadding: Math.round(7 * uiScale)
                            bottomPadding: Math.round(7 * uiScale)
                            leftPadding: Math.round(12 * uiScale)
                            rightPadding: Math.round(12 * uiScale)
                            Keys.onReturnPressed: function(event) {
                                if (!(event.modifiers & Qt.ShiftModifier)) {
                                    event.accepted = true
                                    sendComposer()
                                }
                            }

                            background: Rectangle {
                                radius: Math.round(16 * uiScale)
                                color: "#f6f8fa"
                                border.color: composer.activeFocus ? "#8fbce5" : "#e4eaf0"
                            }
                        }

                        CircleIconButton {
                            uiScale: window.uiScale
                            symbol: bridgeObj && bridgeObj.busy ? "\u2026" : (composerHasText ? "\u27A4" : "\u263A")
                            accent: bridgeObj && bridgeObj.busy ? true : composerHasText
                            enabled: !(bridgeObj && bridgeObj.busy)
                            onClicked: {
                                if (composerHasText) {
                                    sendComposer()
                                } else {
                                    composer.forceActiveFocus()
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Rectangle {
        visible: compactMode && infoDrawerOpen
        anchors.fill: parent
        color: "#55000000"
        z: 4

        MouseArea {
            anchors.fill: parent
            onClicked: infoDrawerOpen = false
        }
    }

    Rectangle {
        visible: infoDrawerOpen
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.topMargin: outerMargin
        anchors.bottomMargin: outerMargin
        anchors.rightMargin: outerMargin
        width: drawerWidth
        radius: sectionRadius
        color: "#f9fbfd"
        border.color: "#dde5eb"
        z: 6

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: Math.round(10 * uiScale)
            spacing: Math.round(6 * uiScale)

            RowLayout {
                Layout.fillWidth: true

                Text {
                    text: "Details"
                    color: "#243744"
                    font.pixelSize: Math.max(15, Math.round(16 * uiScale))
                    font.weight: Font.DemiBold
                }

                Item { Layout.fillWidth: true }

                CircleIconButton {
                    visible: compactMode
                    uiScale: window.uiScale
                    symbol: "X"
                    onClicked: infoDrawerOpen = false
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: "#edf2f6"
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: Math.round(166 * uiScale)
                radius: Math.round(12 * uiScale)
                color: "#ffffff"
                border.color: "#e1e8ee"

                Column {
                    anchors.fill: parent
                    anchors.margins: Math.round(10 * uiScale)
                    spacing: Math.round(6 * uiScale)

                    Rectangle {
                        width: Math.round(72 * uiScale)
                        height: width
                        radius: width / 2
                        color: "#eef3f7"
                        border.color: "#dde5ec"

                        Image {
                            anchors.fill: parent
                            anchors.margins: 3
                            source: bridgeObj ? bridgeObj.heroImage : ""
                            fillMode: Image.PreserveAspectCrop
                            smooth: true
                            clip: true
                        }
                    }

                    Text {
                        text: bridgeObj ? bridgeObj.agentName : "GirlAgent"
                        color: "#243744"
                        font.pixelSize: Math.max(16, Math.round(17 * uiScale))
                        font.weight: Font.DemiBold
                    }

                    Text {
                        text: bridgeObj ? bridgeObj.subtitle : ""
                        color: "#7a8a97"
                        font.pixelSize: Math.max(10, Math.round(11 * uiScale))
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: "#edf2f6"
            }

            StatCard { Layout.fillWidth: true; uiScale: window.uiScale; title: "Mood"; value: bridgeObj ? bridgeObj.mood : "" }
            StatCard { Layout.fillWidth: true; uiScale: window.uiScale; title: "Trust"; value: bridgeObj ? bridgeObj.trust : "" }
            StatCard { Layout.fillWidth: true; uiScale: window.uiScale; title: "Focus"; value: bridgeObj ? bridgeObj.focus : "" }
            StatCard { Layout.fillWidth: true; uiScale: window.uiScale; title: "Recent"; value: bridgeObj ? bridgeObj.recentEvent : "" }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: Math.round(12 * uiScale)
                color: "#ffffff"
                border.color: "#e1e8ee"

                Column {
                    anchors.fill: parent
                    anchors.margins: Math.round(10 * uiScale)
                    spacing: Math.round(6 * uiScale)

                    Text {
                        text: "Session note"
                        color: "#7c8b98"
                        font.pixelSize: Math.max(11, Math.round(12 * uiScale))
                    }

                    Text {
                        width: parent.width
                        text: bridgeObj ? bridgeObj.statusLine : ""
                        wrapMode: Text.Wrap
                        color: "#4f6472"
                        font.pixelSize: Math.max(12, Math.round(13 * uiScale))
                        lineHeight: 1.35
                    }
                }
            }
        }
    }

    Component {
        id: messageDelegate

        MessageBubble {
            role: roleData
            sender: roleData === "assistant" ? (bridgeObj ? bridgeObj.agentName : "GirlAgent") : (roleData === "user" ? "You" : "System")
            text: textData
            tone: toneData
            timestamp: timeData
            groupedWithPrevious: groupedPrevious
            groupedWithNext: groupedNext
            uiScale: window.uiScale
            compact: window.compactMode
            availableWidth: messageView.width
        }
    }

    Component {
        id: dateChipDelegate

        Item {
            width: messageView.width
            height: chip.implicitHeight + Math.round(4 * uiScale)

            DateChip {
                id: chip
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                text: textData
                uiScale: window.uiScale
            }
        }
    }

    Dialog {
        id: confirmationDialog
        modal: true
        anchors.centerIn: parent
        width: Math.max(400, Math.round(460 * uiScale))
        padding: Math.round(24 * uiScale)
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            radius: Math.round(24 * uiScale)
            color: "#ffffff"
            border.color: "#dde5ec"
        }

        Column {
            spacing: Math.round(16 * uiScale)
            width: parent.width

            Text {
                id: confirmationTitle
                color: "#243744"
                font.pixelSize: Math.max(20, Math.round(22 * uiScale))
            }

            Text {
                id: confirmationMessage
                width: parent.width
                wrapMode: Text.Wrap
                color: "#4f6472"
                font.pixelSize: Math.max(14, Math.round(15 * uiScale))
                lineHeight: 1.35
            }

            Row {
                spacing: Math.round(12 * uiScale)

                GhostButton {
                    id: confirmButton
                    scaleRef: uiScale
                    onClicked: {
                        confirmationDialog.close()
                        bridge.resolveConfirmation(true)
                    }
                }

                GhostButton {
                    id: cancelButton
                    scaleRef: uiScale
                    onClicked: {
                        confirmationDialog.close()
                        bridge.resolveConfirmation(false)
                    }
                }
            }
        }
    }

    Dialog {
        id: numberDialog
        property int minimum: 0
        modal: true
        anchors.centerIn: parent
        width: Math.max(400, Math.round(460 * uiScale))
        padding: Math.round(24 * uiScale)
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            radius: Math.round(24 * uiScale)
            color: "#ffffff"
            border.color: "#dde5ec"
        }

        Column {
            spacing: Math.round(16 * uiScale)
            width: parent.width

            Text {
                id: numberTitle
                color: "#243744"
                font.pixelSize: Math.max(20, Math.round(22 * uiScale))
            }

            Text {
                id: numberMessage
                width: parent.width
                wrapMode: Text.Wrap
                color: "#4f6472"
                font.pixelSize: Math.max(14, Math.round(15 * uiScale))
                lineHeight: 1.35
            }

            TextField {
                id: numberField
                width: parent.width
                color: "#243744"
                font.pixelSize: Math.max(14, Math.round(15 * uiScale))
                topPadding: Math.round(12 * uiScale)
                bottomPadding: Math.round(12 * uiScale)
                leftPadding: Math.round(14 * uiScale)
                rightPadding: Math.round(14 * uiScale)
                validator: IntValidator { bottom: numberDialog.minimum }

                background: Rectangle {
                    radius: Math.round(16 * uiScale)
                    color: "#ffffff"
                    border.color: "#dde5ec"
                }
            }

            Row {
                spacing: Math.round(12 * uiScale)

                GhostButton {
                    scaleRef: uiScale
                    text: "Confirm"
                    onClicked: {
                        numberDialog.close()
                        bridge.resolveNumber(parseInt(numberField.text || "0"))
                    }
                }

                GhostButton {
                    scaleRef: uiScale
                    text: "Cancel"
                    onClicked: {
                        numberDialog.close()
                        bridge.resolveNumber(numberDialog.minimum)
                    }
                }
            }
        }
    }
}
