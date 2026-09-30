import math
from tkinter import *


class NodeEditor(Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Editor")
        self.geometry("900x650")

        self.canvas = Canvas(self, bg="#181818", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.onPress)
        self.canvas.bind("<B1-Motion>", self.onDrag)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.canvas.bind("<Motion>", self.onHover)
        self.canvas.bind("<Button-3>", self.onRightClick)

        self.canvas.bind("<MouseWheel>", self.onMouseWheel)
        self.canvas.bind("<Button-4>", self.onMouseWheel)
        self.canvas.bind("<Button-5>", self.onMouseWheel)

        self.canvas.bind("<ButtonPress-2>", self.startPan)
        self.canvas.bind("<B2-Motion>", self.panCanvas)

        self.zoom = 1.0
        self.panX = 0.0
        self.panY = 0.0
        self.gridSize = 20

        self.containers = {}
        self.connections = []  # List of dicts: {"from": (c, n), "to": (c, n), "waypoints": [(logX, logY), ...]}

        self.selectedContainerName = None
        self.selectedConnectionIndex = None  # Tracks currently selected wire
        self.hoveredNode = None
        self.hoveredContainer = None
        self.hoveredWaypoint = None  # (connIndex, waypointIndex)
        self.hoveredConnectionSegment = None  # (connIndex, segmentIndex, snapX, snapY)

        self.draggingWaypoint = None  # (connIndex, waypointIndex)
        self.connectingStartNode = None
        self.connectingWaypoints = []  # List of logical (logX, logY)
        self.connectingMousePos = (0, 0)

        self.dragOffsetGridX = 0.0
        self.dragOffsetGridY = 0.0
        self.dragStartX = 0
        self.dragStartY = 0

        self.nodeScaleAnim = {}
        self.activeAnimators = set()

        self.setupDefaultScene()

    def setupDefaultScene(self):
        self.addContainer("Box1", gridX=3, gridY=2, gridW=5, gridH=4, bgColor="#2A394A", borderColor="#00ADB5")
        self.addContainer("Box2", gridX=-7, gridY=-3, gridW=5, gridH=4, bgColor="#342A4A", borderColor="#BB86FC")

        self.containers["Box1"].addNode("Pin0", -1, 1)
        self.containers["Box1"].addNode("Pin1", -1, 3)
        self.containers["Box1"].addNode("PinOut", 5, 2, bgColor="#00ADB5")

        self.containers["Box2"].addNode("Pin0", -1, 1)
        self.containers["Box2"].addNode("PinOut", 5, 2, bgColor="#BB86FC")

        for cName, container in self.containers.items():
            for nName in container.nodes:
                self.nodeScaleAnim[f"{cName}_{nName}"] = 0.6

        self.addConnection("Box2", "PinOut", "Box1", "Pin0", waypoints=[(-20, -20), (-20, 60)])

        self.update_idletasks()
        self.renderAll()

    def addContainer(self, name, gridX, gridY, gridW, gridH, bgColor="#2D3748", borderColor="#4A5568"):
        container = Container(name, gridX, gridY, gridW, gridH, bgColor, borderColor)
        self.containers[name] = container
        return container

    def snapToMidGrid(self, logX, logY):
        snappedX = (math.floor(logX / self.gridSize) + 0.5) * self.gridSize
        snappedY = (math.floor(logY / self.gridSize) + 0.5) * self.gridSize
        return snappedX, snappedY

    def addConnection(self, fromContainer, fromNode, toContainer, toNode, waypoints=None):
        snappedWaypoints = []
        if waypoints:
            for wx, wy in waypoints:
                snappedWaypoints.append(self.snapToMidGrid(wx, wy))

        conn = {
            "from": (fromContainer, fromNode),
            "to": (toContainer, toNode),
            "waypoints": snappedWaypoints
        }
        self.connections.append(conn)
        self.cleanupWaypoints(len(self.connections) - 1)

    def cleanupWaypoints(self, connIdx):
        if connIdx >= len(self.connections):
            return

        conn = self.connections[connIdx]
        waypoints = conn["waypoints"]
        if not waypoints:
            return

        fromC, fromN = conn["from"]
        toC, toN = conn["to"]
        startLog = self.getNodeCenterLogicalSpace(fromC, fromN)
        endLog = self.getNodeCenterLogicalSpace(toC, toN)

        cleaned = []
        for wp in waypoints:
            snapped = self.snapToMidGrid(wp[0], wp[1])
            # Ignore waypoints that overlap start/end pins or duplicate previous points
            if math.hypot(snapped[0] - startLog[0], snapped[1] - startLog[1]) < self.gridSize * 0.5:
                continue
            if math.hypot(snapped[0] - endLog[0], snapped[1] - endLog[1]) < self.gridSize * 0.5:
                continue
            if not cleaned or cleaned[-1] != snapped:
                cleaned.append(snapped)

        self.connections[connIdx]["waypoints"] = cleaned

    def getCenter(self):
        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 600)
        return w / 2, h / 2, w, h

    def toLogicalSpace(self, winX, winY):
        cx, cy, _, _ = self.getCenter()
        logX = (winX - cx - self.panX) / self.zoom
        logY = (winY - cy - self.panY) / self.zoom
        return logX, logY

    def toWindowSpace(self, logX, logY):
        cx, cy, _, _ = self.getCenter()
        winX = logX * self.zoom + cx + self.panX
        winY = logY * self.zoom + cy + self.panY
        return winX, winY

    def getNodeCenterWindowSpace(self, cName, nName):
        container = self.containers[cName]
        node = container.nodes[nName]
        nLogX = (container.gridX + node.gridX + 0.5) * self.gridSize
        nLogY = (container.gridY + node.gridY + 0.5) * self.gridSize
        return self.toWindowSpace(nLogX, nLogY)

    def getNodeCenterLogicalSpace(self, cName, nName):
        container = self.containers[cName]
        node = container.nodes[nName]
        return (container.gridX + node.gridX + 0.5) * self.gridSize, (container.gridY + node.gridY + 0.5) * self.gridSize

    def findNodeAtPosition(self, winX, winY, maxDistance=20):
        for cName, container in self.containers.items():
            for nName in container.nodes:
                nx, ny = self.getNodeCenterWindowSpace(cName, nName)
                dist = math.hypot(winX - nx, winY - ny)
                if dist <= maxDistance * self.zoom:
                    return (cName, nName)
        return None

    def findWaypointAtPosition(self, winX, winY, maxDistance=14):
        for idx, conn in enumerate(self.connections):
            if idx != self.selectedConnectionIndex:
                continue

            for wpIdx, (wLogX, wLogY) in enumerate(conn["waypoints"]):
                wx, wy = self.toWindowSpace(wLogX, wLogY)
                if math.hypot(winX - wx, winY - wy) <= maxDistance:
                    return (idx, wpIdx)
        return None

    def findConnectionSegmentAtPosition(self, winX, winY, maxDistance=10):
        # Ignore hit test if clicking directly on a pin
        if self.findNodeAtPosition(winX, winY, maxDistance=18):
            return None

        for idx, conn in enumerate(self.connections):
            fromC, fromN = conn["from"]
            toC, toN = conn["to"]
            if fromC not in self.containers or toC not in self.containers:
                continue

            pts = [self.getNodeCenterLogicalSpace(fromC, fromN)] + conn["waypoints"] + [self.getNodeCenterLogicalSpace(toC, toN)]
            winPts = [self.toWindowSpace(px, py) for px, py in pts]

            for segIdx in range(len(winPts) - 1):
                wx1, wy1 = winPts[segIdx]
                wx2, wy2 = winPts[segIdx + 1]

                lineLenSq = (wx2 - wx1)**2 + (wy2 - wy1)**2
                if lineLenSq == 0:
                    continue

                t = max(0, min(1, ((winX - wx1) * (wx2 - wx1) + (winY - wy1) * (wy2 - wy1)) / lineLenSq))
                projWinX = wx1 + t * (wx2 - wx1)
                projWinY = wy1 + t * (wy2 - wy1)

                dist = math.hypot(winX - projWinX, winY - projWinY)

                if dist <= maxDistance:
                    projLogX, projLogY = self.toLogicalSpace(projWinX, projWinY)
                    return (idx, segIdx, projLogX, projLogY)
        return None

    def createRoundedRectPoints(self, x0, y0, x1, y1, radius):
        radius = max(1, min(radius, (x1 - x0) / 2, (y1 - y0) / 2))
        points = []
        corners = [
            (x1 - radius, y0 + radius, 0, 90),
            (x0 + radius, y0 + radius, 90, 180),
            (x0 + radius, y1 - radius, 180, 270),
            (x1 - radius, y1 - radius, 270, 360),
        ]
        for cx, cy, startAngle, endAngle in corners:
            for step in range(startAngle, endAngle + 1, 15):
                rad = math.radians(step)
                points.extend([cx + radius * math.cos(rad), cy - radius * math.sin(rad)])
        return points

    def drawRoundedRect(self, x0, y0, x1, y1, radius, fill, outline, width=2, tags="container"):
        points = self.createRoundedRectPoints(x0, y0, x1, y1, radius)
        return self.canvas.create_polygon(points, fill=fill, outline=outline, width=width, smooth=True, tags=tags)

    def renderGrid(self):
        self.canvas.delete("gridLine")
        _, _, w, h = self.getCenter()

        logLeft, logTop = self.toLogicalSpace(0, 0)
        logRight, logBottom = self.toLogicalSpace(w, h)

        step = self.gridSize
        startX = (int(logLeft) // step) * step
        startY = (int(logTop) // step) * step

        for lx in range(startX, int(logRight) + step, step):
            wx, _ = self.toWindowSpace(lx, 0)
            self.canvas.create_line(wx, 0, wx, h, fill="#222222", tags="gridLine")

        for ly in range(startY, int(logBottom) + step, step):
            _, wy = self.toWindowSpace(0, ly)
            self.canvas.create_line(0, wy, w, wy, fill="#222222", tags="gridLine")

        self.canvas.tag_lower("gridLine")

    def renderConnections(self):
        self.canvas.delete("connection")
        self.canvas.delete("waypoint")

        for idx, conn in enumerate(self.connections):
            fromC, fromN = conn["from"]
            toC, toN = conn["to"]

            if fromC in self.containers and toC in self.containers:
                startWin = self.getNodeCenterWindowSpace(fromC, fromN)
                endWin = self.getNodeCenterWindowSpace(toC, toN)

                points = [startWin[0], startWin[1]]
                for wLogX, wLogY in conn["waypoints"]:
                    wx, wy = self.toWindowSpace(wLogX, wLogY)
                    points.extend([wx, wy])
                points.extend([endWin[0], endWin[1]])

                isSelected = (idx == self.selectedConnectionIndex)
                isSegmentHovered = (self.hoveredConnectionSegment and self.hoveredConnectionSegment[0] == idx)

                wireColor = "#FF2E93" if isSelected else ("#00E5FF" if isSegmentHovered else "#00ADB5")
                wireWidth = max(1, int((4 if isSelected else 3) * self.zoom))

                self.canvas.create_line(
                    points, fill=wireColor, width=wireWidth,
                    capstyle=ROUND, joinstyle=ROUND, tags="connection"
                )

                if isSelected:
                    for wpIdx, (wLogX, wLogY) in enumerate(conn["waypoints"]):
                        wx, wy = self.toWindowSpace(wLogX, wLogY)
                        r = max(4, int(6 * self.zoom))
                        isWpHovered = (self.hoveredWaypoint == (idx, wpIdx))
                        wpColor = "#FFFFFF" if isWpHovered else "#FF2E93"

                        self.canvas.create_oval(
                            wx - r, wy - r, wx + r, wy + r,
                            fill=wpColor, outline="#FFFFFF", width=max(1, int(2 * self.zoom)), tags="waypoint"
                        )

        if self.connectingStartNode:
            cName, nName = self.connectingStartNode
            startWin = self.getNodeCenterWindowSpace(cName, nName)

            pts = [startWin[0], startWin[1]]
            for wLogX, wLogY in self.connectingWaypoints:
                wx, wy = self.toWindowSpace(wLogX, wLogY)
                pts.extend([wx, wy])

            pts.extend([self.connectingMousePos[0], self.connectingMousePos[1]])

            self.canvas.create_line(
                pts, fill="#FF2E93", width=max(1, int(2 * self.zoom)),
                dash=(4, 4), capstyle=ROUND, joinstyle=ROUND, tags="connection"
            )

            for wLogX, wLogY in self.connectingWaypoints:
                wx, wy = self.toWindowSpace(wLogX, wLogY)
                r = max(3, int(5 * self.zoom))
                self.canvas.create_oval(
                    wx - r, wy - r, wx + r, wy + r,
                    fill="#FF2E93", outline="#FFFFFF", width=1, tags="waypoint"
                )

    def renderAll(self):
        self.canvas.delete("all")
        self.renderGrid()
        self.renderConnections()

        cornerRadiusPixels = self.gridSize * 0.4 * self.zoom
        borderWidth = max(1, int(2 * self.zoom))

        for cName, container in self.containers.items():
            cLogX = container.gridX * self.gridSize
            cLogY = container.gridY * self.gridSize
            cLogW = container.gridW * self.gridSize
            cLogH = container.gridH * self.gridSize

            wx0, wy0 = self.toWindowSpace(cLogX, cLogY)
            wx1, wy1 = self.toWindowSpace(cLogX + cLogW, cLogY + cLogH)

            isSelected = cName == self.selectedContainerName

            container.canvasId = self.drawRoundedRect(
                wx0, wy0, wx1, wy1,
                radius=cornerRadiusPixels,
                fill=container.bgColor,
                outline=container.borderColor if not isSelected else "#FFFFFF",
                width=borderWidth,
                tags=("container", f"container_{cName}")
            )

            for nName, node in container.nodes.items():
                nodeKey = f"{cName}_{nName}"
                currentScale = self.nodeScaleAnim.get(nodeKey, 0.6)

                scaledSize = self.gridSize * currentScale
                offset = (self.gridSize - scaledSize) / 2

                nLogX = (container.gridX + node.gridX) * self.gridSize + offset
                nLogY = (container.gridY + node.gridY) * self.gridSize + offset

                nWx0, nWy0 = self.toWindowSpace(nLogX, nLogY)
                nWx1, nWy1 = self.toWindowSpace(nLogX + scaledSize, nLogY + scaledSize)

                pinRadius = (scaledSize * 0.25) * self.zoom
                isNodeHovered = (self.hoveredNode == (cName, nName))

                if isNodeHovered or currentScale > 0.6:
                    glowPoints = self.createRoundedRectPoints(nWx0, nWy0, nWx1, nWy1, pinRadius)
                    self.canvas.create_polygon(
                        glowPoints, fill="", outline="#FFFFFF", width=int(2 * self.zoom), smooth=True, tags="nodeGlow"
                    )

                node.canvasId = self.drawRoundedRect(
                    nWx0, nWy0, nWx1, nWy1,
                    radius=pinRadius,
                    fill=node.bgColor,
                    outline=node.borderColor,
                    width=borderWidth,
                    tags=("node", f"node_{cName}_{nName}")
                )

        self.canvas.tag_lower("connection")
        self.canvas.tag_lower("gridLine")

    def animateNodeScale(self, cName, nName, targetScale):
        nodeKey = f"{cName}_{nName}"

        def stepAnimation():
            currentScale = self.nodeScaleAnim.get(nodeKey, 0.6)
            if abs(currentScale - targetScale) < 0.02:
                self.nodeScaleAnim[nodeKey] = targetScale
                self.activeAnimators.discard(nodeKey)
                self.renderAll()
                return

            newScale = currentScale + (targetScale - currentScale) * 0.35
            self.nodeScaleAnim[nodeKey] = newScale
            self.renderAll()
            self.after(16, stepAnimation)

        if nodeKey not in self.activeAnimators:
            self.activeAnimators.add(nodeKey)
            stepAnimation()

    def onHover(self, event):
        if self.draggingWaypoint:
            connIdx, wpIdx = self.draggingWaypoint
            logX, logY = self.toLogicalSpace(event.x, event.y)
            snappedX, snappedY = self.snapToMidGrid(logX, logY)
            self.connections[connIdx]["waypoints"][wpIdx] = (snappedX, snappedY)
            self.renderAll()
            return

        self.hoveredNode = self.findNodeAtPosition(event.x, event.y, maxDistance=18)
        self.hoveredWaypoint = self.findWaypointAtPosition(event.x, event.y, maxDistance=14)
        self.hoveredConnectionSegment = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=10)

        newHoveredContainer = None
        if not self.hoveredNode and not self.hoveredWaypoint and not self.hoveredConnectionSegment:
            clickedItems = self.canvas.find_withtag("current")
            if clickedItems:
                tags = self.canvas.gettags(clickedItems[0])
                for tag in tags:
                    if tag.startswith("container_"):
                        newHoveredContainer = tag.split("_", 1)[1]

        for cName, container in self.containers.items():
            for nName in container.nodes:
                nodeKey = f"{cName}_{nName}"
                targetScale = 1.0 if self.hoveredNode == (cName, nName) else 0.6
                if self.nodeScaleAnim.get(nodeKey, 0.6) != targetScale:
                    self.animateNodeScale(cName, nName, targetScale)

        if newHoveredContainer != self.hoveredContainer or self.connectingStartNode:
            self.hoveredContainer = newHoveredContainer

        self.connectingMousePos = (event.x, event.y)
        self.renderAll()

    def onRightClick(self, event):
        if self.connectingStartNode:
            self.connectingStartNode = None
            self.connectingWaypoints.clear()
            self.renderAll()
            return

        wp = self.findWaypointAtPosition(event.x, event.y, maxDistance=14)
        if wp:
            connIdx, wpIdx = wp
            self.connections[connIdx]["waypoints"].pop(wpIdx)
            self.hoveredWaypoint = None
            self.renderAll()
            return

        seg = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=10)
        if seg:
            connIdx, _, _, _ = seg
            self.connections.pop(connIdx)
            self.selectedConnectionIndex = None
            self.hoveredConnectionSegment = None
            self.renderAll()

    def onPress(self, event):
        # PRIORITY 1: Click directly on a Pin/Node
        nodeAtPress = self.findNodeAtPosition(event.x, event.y, maxDistance=18)
        if nodeAtPress:
            if not self.connectingStartNode:
                self.connectingStartNode = nodeAtPress
                self.connectingWaypoints = []
            else:
                if nodeAtPress != self.connectingStartNode:
                    startC, startN = self.connectingStartNode
                    targetC, targetN = nodeAtPress
                    self.addConnection(startC, startN, targetC, targetN, waypoints=list(self.connectingWaypoints))
                    self.connectingStartNode = None
                    self.connectingWaypoints.clear()
            self.renderAll()
            return

        # PRIORITY 2: Click on an existing Waypoint handle to drag it
        wp = self.findWaypointAtPosition(event.x, event.y, maxDistance=14)
        if wp:
            self.draggingWaypoint = wp
            return

        # PRIORITY 3: Left-click on an existing wire segment to split/add a waypoint
        seg = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=10)
        if seg and not self.connectingStartNode:
            connIdx, segIdx, projX, projY = seg
            snappedX, snappedY = self.snapToMidGrid(projX, projY)

            self.selectedConnectionIndex = connIdx
            self.connections[connIdx]["waypoints"].insert(segIdx, (snappedX, snappedY))
            self.cleanupWaypoints(connIdx)
            self.draggingWaypoint = (connIdx, segIdx)
            self.renderAll()
            return

        # PRIORITY 4: Click open space while drawing wire to place turning point
        if self.connectingStartNode:
            logX, logY = self.toLogicalSpace(event.x, event.y)
            snappedX, snappedY = self.snapToMidGrid(logX, logY)
            if not self.connectingWaypoints or self.connectingWaypoints[-1] != (snappedX, snappedY):
                self.connectingWaypoints.append((snappedX, snappedY))
            self.renderAll()
            return

        # PRIORITY 5: Click container to select/drag
        clickedItems = self.canvas.find_withtag("current")
        if clickedItems and "container" in self.canvas.gettags(clickedItems[0]):
            clickedId = clickedItems[0]
            for name, container in self.containers.items():
                if container.canvasId == clickedId:
                    self.selectedContainerName = name
                    break

            if self.selectedContainerName:
                container = self.containers.pop(self.selectedContainerName)
                self.containers[self.selectedContainerName] = container

                mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)
                mouseGridX = mouseLogX / self.gridSize
                mouseGridY = mouseLogY / self.gridSize

                self.dragOffsetGridX = mouseGridX - container.gridX
                self.dragOffsetGridY = mouseGridY - container.gridY
                self.selectedConnectionIndex = None
                self.renderAll()
                return

        # Click open space -> Deselect wire
        self.selectedConnectionIndex = None
        self.renderAll()

    def onDrag(self, event):
        if self.draggingWaypoint:
            connIdx, wpIdx = self.draggingWaypoint
            logX, logY = self.toLogicalSpace(event.x, event.y)
            snappedX, snappedY = self.snapToMidGrid(logX, logY)
            self.connections[connIdx]["waypoints"][wpIdx] = (snappedX, snappedY)
            self.renderAll()
            return

        if self.connectingStartNode:
            self.connectingMousePos = (event.x, event.y)
            self.renderAll()
            return

        if self.selectedContainerName:
            container = self.containers[self.selectedContainerName]
            mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)

            mouseGridX = mouseLogX / self.gridSize
            mouseGridY = mouseLogY / self.gridSize

            targetGridX = mouseGridX - self.dragOffsetGridX
            targetGridY = mouseGridY - self.dragOffsetGridY

            snapGridX = round(targetGridX)
            snapGridY = round(targetGridY)

            if container.gridX != snapGridX or container.gridY != snapGridY:
                container.gridX = snapGridX
                container.gridY = snapGridY
                self.renderAll()

    def onRelease(self, event):
        if self.draggingWaypoint:
            connIdx, _ = self.draggingWaypoint
            self.cleanupWaypoints(connIdx)
            self.draggingWaypoint = None

        self.selectedContainerName = None
        self.renderAll()

    def onMouseWheel(self, event):
        cx, cy, _, _ = self.getCenter()
        scaleFactor = 1.1 if (event.num == 4 or event.delta > 0) else 0.9

        mx, my = event.x, event.y
        self.panX = (mx - cx) - scaleFactor * (mx - cx - self.panX)
        self.panY = (my - cy) - scaleFactor * (my - cy - self.panY)
        self.zoom *= scaleFactor
        self.renderAll()

    def startPan(self, event):
        self.dragStartX = event.x
        self.dragStartY = event.y

    def panCanvas(self, event):
        dx = event.x - self.dragStartX
        dy = event.y - self.dragStartY
        self.panX += dx
        self.panY += dy
        self.dragStartX = event.x
        self.dragStartY = event.y
        self.renderAll()


class Container:
    def __init__(self, name, gridX, gridY, gridW, gridH, bgColor="#2D3748", borderColor="#4A5568"):
        self.name = name
        self.gridX = float(gridX)
        self.gridY = float(gridY)
        self.gridW = float(gridW)
        self.gridH = float(gridH)
        self.bgColor = bgColor
        self.borderColor = borderColor
        self.canvasId = None
        self.nodes = {}

    def addNode(self, name, gridX, gridY, bgColor="#1A202C", borderColor="#A0AEC0"):
        self.nodes[name] = Node(name, int(gridX), int(gridY), bgColor=bgColor, borderColor=borderColor)


class Node:
    def __init__(self, name, gridX, gridY, bgColor="#1A202C", borderColor="#A0AEC0"):
        self.name = name
        self.gridX = int(gridX)
        self.gridY = int(gridY)
        self.bgColor = bgColor
        self.borderColor = borderColor
        self.canvasId = None


if __name__ == "__main__":
    app = NodeEditor()
    app.mainloop()