import math
from tkinter import *
from typing import Dict, List, Tuple, Optional, Any


class ChildrenModel:
    def __init__(self, name: str, grid_x: float, grid_y: float, grid_w: float, grid_h: float,
                 svg_data: str = "", bg_color: str = "transparent", border_color: str = "transparent"):
        self.name = name
        self.gridX = float(grid_x)
        self.gridY = float(grid_y)
        self.gridW = float(grid_w)
        self.gridH = float(grid_h)
        self.svg_data = svg_data
        self.bg_color = bg_color
        self.border_color = border_color
        self.canvasId = None


class NodeModel:
    def __init__(self, name: str, grid_x: int, grid_y: int, bg_color: str = "#1A202C", border_color: str = "#A0AEC0"):
        self.name = name
        self.gridX = int(grid_x)
        self.gridY = int(grid_y)
        self.bg_color = bg_color
        self.border_color = border_color
        self.canvasId = None


class ContainerModel:
    def __init__(self, parent_editor, name: str, grid_x: float, grid_y: float, grid_w: float, grid_h: float,
                 bg_color: str = "#2D3748", border_color: str = "#4A5568"):
        self.parent = parent_editor
        self.name = name
        self.gridX = float(grid_x)
        self.gridY = float(grid_y)
        self.gridW = float(grid_w)
        self.gridH = float(grid_h)
        self.bg_color = bg_color
        self.border_color = border_color
        self.canvasId = None
        self.nodes: Dict[str, NodeModel] = {}
        self.children: Dict[str, ChildrenModel] = {}

    def addNode(self, name: str, gridX: int, gridY: int, bg_color: str = "#1A202C", border_color: str = "#A0AEC0") -> NodeModel:
        node = NodeModel(name, gridX, gridY, bg_color=bg_color, border_color=border_color)
        self.nodes[name] = node
        if hasattr(self.parent, "nodeScaleAnim"):
            self.parent.nodeScaleAnim[f"{self.name}_{name}"] = 0.6
        return node

    def addChild(self, name: str, gridX: float, gridY: float, gridW: float, gridH: float,
                 svg_data: str = "", bg_color: str = "transparent", border_color: str = "transparent") -> ChildrenModel:
        child = ChildrenModel(name, gridX, gridY, gridW, gridH, svg_data=svg_data, bg_color=bg_color, border_color=border_color)
        self.children[name] = child
        return child


Container = ContainerModel
Node = NodeModel
Children = ChildrenModel


class NodeEditor(Tk):
    def __init__(self, master=None):
        if master is None:
            super().__init__()
            self.title("Node Editor")
            self.geometry("900x650")
            self.root = self
        else:
            self.root = master

        self.canvas = Canvas(self.root, bg="#181818", highlightthickness=0)
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

        self.containers: Dict[str, ContainerModel] = {}
        self.connections: List[Dict[str, Any]] = []
        self.selectedContainerName = None
        self.selectedConnectionIndex = None
        self.hoveredNode = None
        self.hoveredWaypoint = None
        self.hoveredConnectionSegment = None
        self.draggingWaypoint = None

        self.connectingStart = None
        self.connectingWaypoints = []
        self.connectingMousePos = (0, 0)

        self.dragOffsetGridX = 0.0
        self.dragOffsetGridY = 0.0
        self.dragStartX = 0
        self.dragStartY = 0

        self.nodeScaleAnim = {}
        self.activeAnimators = set()

    def addContainer(self, name: str, gridX: float, gridY: float, gridW: float, gridH: float,
                     bg_color: str = "#2D3748", border_color: str = "#4A5568") -> ContainerModel:
        container = ContainerModel(self, name, gridX, gridY, gridW, gridH, bg_color, border_color)
        self.containers[name] = container
        return container

    def addConnection(self, fromContainer: str, fromNode: str, toContainer: str, toNode: str, waypoints: Optional[List[Tuple[float, float]]] = None):
        if waypoints is None:
            fromX, fromY = self.getNodeCenterLogicalSpace(fromContainer, fromNode)
            toX, toY = self.getNodeCenterLogicalSpace(toContainer, toNode)
            midX, _ = self.snapToMidGrid((fromX + toX) / 2, 0)
            waypoints = [(midX, fromY), (midX, toY)]

        self.connections.append({
            "from": (fromContainer, fromNode),
            "branches": [
                {
                    "waypoints": waypoints,
                    "to": (toContainer, toNode),
                    "sub_branches": []
                }
            ],
            "Activated": True
        })

    def snapToMidGrid(self, logX: float, logY: float) -> Tuple[float, float]:
        snappedX = (math.floor(logX / self.gridSize) + 0.5) * self.gridSize
        snappedY = (math.floor(logY / self.gridSize) + 0.5) * self.gridSize
        return snappedX, snappedY

    def getCenter(self) -> Tuple[float, float, int, int]:
        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 600)
        return w / 2, h / 2, w, h

    def toLogicalSpace(self, winX: float, winY: float) -> Tuple[float, float]:
        cx, cy, _, _ = self.getCenter()
        logX = (winX - cx - self.panX) / self.zoom
        logY = (winY - cy - self.panY) / self.zoom
        return logX, logY

    def toWindowSpace(self, logX: float, logY: float) -> Tuple[float, float]:
        cx, cy, _, _ = self.getCenter()
        winX = logX * self.zoom + cx + self.panX
        winY = logY * self.zoom + cy + self.panY
        return winX, winY

    def getNodeCenterWindowSpace(self, cName: str, nName: str) -> Tuple[float, float]:
        container = self.containers[cName]
        node = container.nodes[nName]
        nLogX = (container.gridX + node.gridX + 0.5) * self.gridSize
        nLogY = (container.gridY + node.gridY + 0.5) * self.gridSize
        return self.toWindowSpace(nLogX, nLogY)

    def getNodeCenterLogicalSpace(self, cName: str, nName: str) -> Tuple[float, float]:
        container = self.containers[cName]
        node = container.nodes[nName]
        return (container.gridX + node.gridX + 0.5) * self.gridSize, (container.gridY + node.gridY + 0.5) * self.gridSize

    def findNodeAtPosition(self, winX: float, winY: float, maxDistance: float = 10):
        for cName, container in self.containers.items():
            for nName in container.nodes:
                nx, ny = self.getNodeCenterWindowSpace(cName, nName)
                dist = math.hypot(winX - nx, winY - ny)
                if dist <= maxDistance * self.zoom:
                    return (cName, nName)
        return None

    def findWaypointAtPosition(self, winX: float, winY: float, maxDistance: float = 8):
        for idx, conn in enumerate(self.connections):
            def searchBranch(branch):
                for wpIdx, (wLogX, wLogY) in enumerate(branch["waypoints"]):
                    wx, wy = self.toWindowSpace(wLogX, wLogY)
                    if math.hypot(winX - wx, winY - wy) <= maxDistance:
                        return (idx, branch, wpIdx)
                for sb in branch.get("sub_branches", []):
                    res = searchBranch(sb)
                    if res:
                        return res
                return None

            for branch in conn["branches"]:
                res = searchBranch(branch)
                if res:
                    return res
        return None

    def findConnectionSegmentAtPosition(self, winX: float, winY: float, maxDistance: float = 5):
        if self.findNodeAtPosition(winX, winY, maxDistance=6):
            return None

        for idx, conn in enumerate(self.connections):
            fromC, fromN = conn["from"]
            if fromC not in self.containers:
                continue
            startLog = self.getNodeCenterLogicalSpace(fromC, fromN)

            def checkBranchSegments(startPoint, branch):
                pts = [startPoint] + branch["waypoints"]
                if "to" in branch and branch["to"][0] in self.containers:
                    pts.append(self.getNodeCenterLogicalSpace(*branch["to"]))

                winPts = [self.toWindowSpace(px, py) for px, py in pts]

                for segIdx in range(len(winPts) - 1):
                    wx1, wy1 = winPts[segIdx]
                    wx2, wy2 = winPts[segIdx + 1]

                    lineLenSq = (wx2 - wx1) ** 2 + (wy2 - wy1) ** 2
                    if lineLenSq == 0:
                        continue

                    t = max(0, min(1, ((winX - wx1) * (wx2 - wx1) + (winY - wy1) * (wy2 - wy1)) / lineLenSq))
                    projWinX = wx1 + t * (wx2 - wx1)
                    projWinY = wy1 + t * (wy2 - wy1)

                    if math.hypot(winX - projWinX, winY - projWinY) <= maxDistance:
                        projLogX, projLogY = self.toLogicalSpace(projWinX, projWinY)
                        return (idx, branch, segIdx, projLogX, projLogY)

                for sb in branch.get("sub_branches", []):
                    tapPt = branch["waypoints"][sb["tap_waypoint_idx"]] if sb["tap_waypoint_idx"] < len(branch["waypoints"]) else startPoint
                    res = checkBranchSegments(tapPt, sb)
                    if res:
                        return res
                return None

            for bIdx, branch in enumerate(conn["branches"]):
                res = checkBranchSegments(startLog, branch)
                if res:
                    return res

        return None

    def insertWaypointInBranch(self, branch, segIdx, coord):
        branch["waypoints"].insert(segIdx, coord)
        for sb in branch.get("sub_branches", []):
            if sb["tap_waypoint_idx"] >= segIdx:
                sb["tap_waypoint_idx"] += 1

    def removeWaypointFromBranch(self, branch, wpIdx):
        if wpIdx < len(branch["waypoints"]):
            branch["waypoints"].pop(wpIdx)
            subs_to_keep = []
            for sb in branch.get("sub_branches", []):
                if sb["tap_waypoint_idx"] > wpIdx:
                    sb["tap_waypoint_idx"] -= 1
                    subs_to_keep.append(sb)
                elif sb["tap_waypoint_idx"] < wpIdx:
                    subs_to_keep.append(sb)
            branch["sub_branches"] = subs_to_keep

    def renderSvgData(self, svg_str: str, wx0: float, wy0: float, width: float, height: float, tags: Any):
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(svg_str)
        except Exception:
            return

        vb = root.attrib.get("viewBox")
        if vb:
            vx, vy, vw, vh = map(float, vb.split())
        else:
            vx, vy, vw, vh = 0, 0, 100, 100

        scale_x = width / vw if vw else 1
        scale_y = height / vh if vh else 1

        def map_x(x_val):
            return wx0 + (float(x_val) - vx) * scale_x

        def map_y(y_val):
            return wy0 + (float(y_val) - vy) * scale_y

        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            fill = elem.attrib.get("fill", "none")
            stroke = elem.attrib.get("stroke", "none")
            sw_str = elem.attrib.get("stroke-width", "1")
            try:
                sw = float(sw_str) * min(scale_x, scale_y)
            except ValueError:
                sw = 1.0

            fill_val = "" if fill == "none" else fill
            stroke_val = "" if stroke == "none" else stroke

            if tag == "rect":
                rx0 = map_x(elem.attrib.get("x", 0))
                ry0 = map_y(elem.attrib.get("y", 0))
                rx1 = rx0 + float(elem.attrib.get("width", 0)) * scale_x
                ry1 = ry0 + float(elem.attrib.get("height", 0)) * scale_y
                self.canvas.create_rectangle(rx0, ry0, rx1, ry1, fill=fill_val, outline=stroke_val, width=sw, tags=tags)

            elif tag == "circle":
                cx_v = map_x(elem.attrib.get("cx", 0))
                cy_v = map_y(elem.attrib.get("cy", 0))
                r_v = float(elem.attrib.get("r", 0)) * scale_x
                self.canvas.create_oval(cx_v - r_v, cy_v - r_v, cx_v + r_v, cy_v + r_v, fill=fill_val, outline=stroke_val, width=sw, tags=tags)

            elif tag == "ellipse":
                cx_v = map_x(elem.attrib.get("cx", 0))
                cy_v = map_y(elem.attrib.get("cy", 0))
                rx_v = float(elem.attrib.get("rx", 0)) * scale_x
                ry_v = float(elem.attrib.get("ry", 0)) * scale_y
                self.canvas.create_oval(cx_v - rx_v, cy_v - ry_v, cx_v + rx_v, cy_v + ry_v, fill=fill_val, outline=stroke_val, width=sw, tags=tags)

            elif tag == "line":
                lx1 = map_x(elem.attrib.get("x1", 0))
                ly1 = map_y(elem.attrib.get("y1", 0))
                lx2 = map_x(elem.attrib.get("x2", 0))
                ly2 = map_y(elem.attrib.get("y2", 0))
                self.canvas.create_line(lx1, ly1, lx2, ly2, fill=stroke_val, width=sw, tags=tags)

            elif tag == "polyline" or tag == "polygon":
                pts_raw = elem.attrib.get("points", "").strip().split()
                pts = []
                for p in pts_raw:
                    coords = p.split(",")
                    if len(coords) == 2:
                        pts.extend([map_x(coords[0]), map_y(coords[1])])
                if pts:
                    if tag == "polygon":
                        self.canvas.create_polygon(pts, fill=fill_val, outline=stroke_val, width=sw, tags=tags)
                    else:
                        self.canvas.create_line(pts, fill=stroke_val, width=sw, tags=tags)

            elif tag == "path":
                d = elem.attrib.get("d", "")
                import re
                tokens = re.findall(r'([a-zA-Z])|([-+]?(?:\d*\.\d+|\d+))', d)
                cmd_list = []
                for t in tokens:
                    if t[0]:
                        cmd_list.append(t[0])
                    elif t[1]:
                        cmd_list.append(float(t[1]))

                pts = []
                idx = 0
                while idx < len(cmd_list):
                    c = cmd_list[idx]
                    if isinstance(c, str):
                        idx += 1
                        if c in ['M', 'L']:
                            pts.extend([map_x(cmd_list[idx]), map_y(cmd_list[idx+1])])
                            idx += 2
                    else:
                        pts.extend([map_x(cmd_list[idx]), map_y(cmd_list[idx+1])])
                        idx += 2
                if pts:
                    if fill_val:
                        self.canvas.create_polygon(pts, fill=fill_val, outline=stroke_val, width=sw, tags=tags)
                    else:
                        self.canvas.create_line(pts, fill=stroke_val, width=sw, tags=tags)

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
        fill_val = "" if fill == "transparent" else fill
        outline_val = "" if outline == "transparent" else outline
        return self.canvas.create_polygon(points, fill=fill_val, outline=outline_val, width=width, smooth=True, tags=tags)

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
            if fromC not in self.containers:
                continue
            startWin = self.getNodeCenterWindowSpace(fromC, fromN)

            isSelected = (idx == self.selectedConnectionIndex)
            isHovered = (self.hoveredConnectionSegment and self.hoveredConnectionSegment[0] == idx)
            isActivated = conn.get("Activated", True)

            wireColor = "#FF2E93" if isSelected else ("#00E5FF" if isHovered else ("#00ADB5" if isActivated else "#555555"))
            wireWidth = max(1, int((4 if isSelected else 3) * self.zoom))

            def drawBranchTree(startPtWin, branch):
                pts = [startPtWin[0], startPtWin[1]]
                for wLogX, wLogY in branch["waypoints"]:
                    wx, wy = self.toWindowSpace(wLogX, wLogY)
                    pts.extend([wx, wy])

                if "to" in branch and branch["to"][0] in self.containers:
                    endWin = self.getNodeCenterWindowSpace(*branch["to"])
                    pts.extend([endWin[0], endWin[1]])

                self.canvas.create_line(
                    pts, fill=wireColor, width=wireWidth,
                    capstyle=ROUND, joinstyle=ROUND, tags="connection"
                )

                for wpIdx, (wLogX, wLogY) in enumerate(branch["waypoints"]):
                    isWpHovered = (self.hoveredWaypoint and self.hoveredWaypoint[0] == idx and self.hoveredWaypoint[1] is branch and self.hoveredWaypoint[2] == wpIdx)

                    if isSelected or isWpHovered or isHovered:
                        wx, wy = self.toWindowSpace(wLogX, wLogY)
                        r = max(3, int(5 * self.zoom))
                        dotFill = "#FFFFFF" if isWpHovered else "#00ADB5"
                        self.canvas.create_oval(
                            wx - r, wy - r, wx + r, wy + r,
                            fill=dotFill, outline="#FFFFFF", width=max(1, int(1.5 * self.zoom)), tags="waypoint"
                        )

                for sb in branch.get("sub_branches", []):
                    if sb["tap_waypoint_idx"] < len(branch["waypoints"]):
                        tapWp = branch["waypoints"][sb["tap_waypoint_idx"]]
                        tapWin = self.toWindowSpace(*tapWp)
                        drawBranchTree(tapWin, sb)

            for branch in conn["branches"]:
                drawBranchTree(startWin, branch)

        if self.connectingStart:
            if self.connectingStart["mode"] == "new_tree":
                startWin = self.getNodeCenterWindowSpace(*self.connectingStart["from"])
            elif self.connectingStart["mode"] == "branch_tree":
                parentBranch = self.connectingStart["parentBranch"]
                tapIdx = self.connectingStart["tapIdx"]
                tapLog = parentBranch["waypoints"][tapIdx]
                startWin = self.toWindowSpace(*tapLog)

            pts = [startWin[0], startWin[1]]
            for wLogX, wLogY in self.connectingWaypoints:
                wx, wy = self.toWindowSpace(wLogX, wLogY)
                pts.extend([wx, wy])
            pts.extend([self.connectingMousePos[0], self.connectingMousePos[1]])

            self.canvas.create_line(
                pts, fill="#FF2E93", width=max(1, int(2 * self.zoom)),
                dash=(4, 4), capstyle=ROUND, joinstyle=ROUND, tags="connection"
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
                fill=container.bg_color,
                outline=container.border_color if not isSelected else "#FFFFFF",
                width=borderWidth,
                tags=("container", f"container_{cName}")
            )

            for chName, child in container.children.items():
                chLogX = (container.gridX + child.gridX) * self.gridSize
                chLogY = (container.gridY + child.gridY) * self.gridSize
                chLogW = child.gridW * self.gridSize
                chLogH = child.gridH * self.gridSize

                chWx0, chWy0 = self.toWindowSpace(chLogX, chLogY)
                chWx1, chWy1 = self.toWindowSpace(chLogX + chLogW, chLogY + chLogH)

                w_px = chWx1 - chWx0
                h_px = chWy1 - chWy0

                if child.bg_color != "transparent" or child.border_color != "transparent":
                    child.canvasId = self.drawRoundedRect(
                        chWx0, chWy0, chWx1, chWy1,
                        radius=4 * self.zoom,
                        fill=child.bg_color,
                        outline=child.border_color,
                        width=borderWidth,
                        tags=("child", f"child_{cName}_{chName}")
                    )

                if child.svg_data:
                    self.renderSvgData(child.svg_data, chWx0, chWy0, w_px, h_px, tags=("child_svg", f"svg_{cName}_{chName}"))

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
                    fill=node.bg_color,
                    outline=node.border_color,
                    width=borderWidth,
                    tags=("node", f"node_{cName}_{nName}")
                )
                self.canvas.create_text(
                    (nWx0 + nWx1) / 2,
                    (nWy0 + nWy1) / 2,
                    fill="white",
                    font=("Arial", int(borderWidth * 1.2), "bold"),
                    text=node.name
                )

        self.canvas.tag_lower("connection")
        self.canvas.tag_lower("gridLine")

    def animateNodeScale(self, cName: str, nName: str, targetScale: float):
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
            connIdx, branch, wpIdx = self.draggingWaypoint
            logX, logY = self.toLogicalSpace(event.x, event.y)
            snappedX, snappedY = self.snapToMidGrid(logX, logY)
            branch["waypoints"][wpIdx] = (snappedX, snappedY)
            self.renderAll()
            return

        self.hoveredNode = self.findNodeAtPosition(event.x, event.y, maxDistance=8)
        self.hoveredWaypoint = self.findWaypointAtPosition(event.x, event.y, maxDistance=6)
        self.hoveredConnectionSegment = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=5)

        for cName, container in self.containers.items():
            for nName in container.nodes:
                nodeKey = f"{cName}_{nName}"
                targetScale = 1.0 if self.hoveredNode == (cName, nName) else 0.6
                if self.nodeScaleAnim.get(nodeKey, 0.6) != targetScale:
                    self.animateNodeScale(cName, nName, targetScale)

        self.connectingMousePos = (event.x, event.y)
        self.renderAll()

    def onRightClick(self, event):
        if self.connectingStart:
            self.connectingStart = None
            self.connectingWaypoints.clear()
            self.renderAll()
            return

        wp = self.findWaypointAtPosition(event.x, event.y, maxDistance=8)
        if wp:
            connIdx, branch, wpIdx = wp
            self.removeWaypointFromBranch(branch, wpIdx)
            self.hoveredWaypoint = None
            self.renderAll()
            return

        seg = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=5)
        if seg:
            connIdx = seg[0]
            self.connections.pop(connIdx)
            self.selectedConnectionIndex = None
            self.hoveredConnectionSegment = None
            self.renderAll()

    def onPress(self, event):
        nodeAtPress = self.findNodeAtPosition(event.x, event.y, maxDistance=10)
        if nodeAtPress:
            if not self.connectingStart:
                self.connectingStart = {
                    "mode": "new_tree",
                    "from": nodeAtPress
                }
                self.connectingWaypoints = []
            else:
                if self.connectingStart["mode"] == "new_tree":
                    wps = list(self.connectingWaypoints)
                    if not wps:
                        wps = []

                    self.connections.append({
                        "from": self.connectingStart["from"],
                        "branches": [
                            {
                                "waypoints": wps,
                                "to": nodeAtPress,
                                "sub_branches": []
                            }
                        ],
                        "Activated": True
                    })
                elif self.connectingStart["mode"] == "branch_tree":
                    parentBranch = self.connectingStart["parentBranch"]
                    tapIdx = self.connectingStart["tapIdx"]

                    newBranch = {
                        "tap_waypoint_idx": tapIdx,
                        "waypoints": list(self.connectingWaypoints),
                        "to": nodeAtPress,
                        "sub_branches": []
                    }
                    parentBranch.setdefault("sub_branches", []).append(newBranch)

                self.connectingStart = None
                self.connectingWaypoints.clear()
            self.renderAll()
            return

        if event.state & 0x0001:
            wp = self.findWaypointAtPosition(event.x, event.y, maxDistance=8)
            if wp and not self.connectingStart:
                connIdx, branch, wpIdx = wp
                self.connectingStart = {
                    "mode": "branch_tree",
                    "connIdx": connIdx,
                    "parentBranch": branch,
                    "tapIdx": wpIdx
                }
                self.connectingWaypoints = []
                self.renderAll()
                return

            seg = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=6)
            if seg and not self.connectingStart:
                connIdx, parent_branch, segIdx, projX, projY = seg
                snapped = self.snapToMidGrid(projX, projY)

                self.insertWaypointInBranch(parent_branch, segIdx, snapped)

                self.connectingStart = {
                    "mode": "branch_tree",
                    "connIdx": connIdx,
                    "parentBranch": parent_branch,
                    "tapIdx": segIdx
                }
                self.connectingWaypoints = []
                self.renderAll()
                return

        wp = self.findWaypointAtPosition(event.x, event.y, maxDistance=8)
        if wp and not self.connectingStart:
            connIdx, branch, wpIdx = wp
            self.selectedConnectionIndex = connIdx
            self.draggingWaypoint = (connIdx, branch, wpIdx)
            self.renderAll()
            return

        seg = self.findConnectionSegmentAtPosition(event.x, event.y, maxDistance=5)
        if seg and not self.connectingStart:
            connIdx, branch, segIdx, projX, projY = seg
            snapped = self.snapToMidGrid(projX, projY)

            self.selectedConnectionIndex = connIdx
            self.insertWaypointInBranch(branch, segIdx, snapped)
            self.draggingWaypoint = (connIdx, branch, segIdx)
            self.renderAll()
            return

        if self.connectingStart:
            logX, logY = self.toLogicalSpace(event.x, event.y)
            snapped = self.snapToMidGrid(logX, logY)
            if not self.connectingWaypoints or self.connectingWaypoints[-1] != snapped:
                self.connectingWaypoints.append(snapped)
            self.renderAll()
            return

        clickedItems = self.canvas.find_withtag("current")
        if clickedItems and ("container" in self.canvas.gettags(clickedItems[0]) or "child" in self.canvas.gettags(clickedItems[0]) or "child_svg" in self.canvas.gettags(clickedItems[0])):
            clickedId = clickedItems[0]
            tags = self.canvas.gettags(clickedId)

            target_container_name = None
            for tag in tags:
                if tag.startswith("container_"):
                    target_container_name = tag.replace("container_", "")
                    break
                elif tag.startswith("child_"):
                    target_container_name = tag.split("_")[1]
                    break
                elif tag.startswith("svg_"):
                    target_container_name = tag.split("_")[1]
                    break

            if target_container_name and target_container_name in self.containers:
                self.selectedContainerName = target_container_name
                container = self.containers.pop(self.selectedContainerName)
                self.containers[self.selectedContainerName] = container

                mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)
                self.dragOffsetGridX = (mouseLogX / self.gridSize) - container.gridX
                self.dragOffsetGridY = (mouseLogY / self.gridSize) - container.gridY
                self.selectedConnectionIndex = None
                self.renderAll()
                return

        self.selectedConnectionIndex = None
        self.renderAll()

    def onDrag(self, event):
        if self.draggingWaypoint:
            connIdx, branch, wpIdx = self.draggingWaypoint
            logX, logY = self.toLogicalSpace(event.x, event.y)
            snappedX, snappedY = self.snapToMidGrid(logX, logY)
            branch["waypoints"][wpIdx] = (snappedX, snappedY)
            self.renderAll()
            return

        if self.connectingStart:
            self.connectingMousePos = (event.x, event.y)
            self.renderAll()
            return

        if self.selectedContainerName:
            container = self.containers[self.selectedContainerName]
            mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)

            snapGridX = round((mouseLogX / self.gridSize) - self.dragOffsetGridX)
            snapGridY = round((mouseLogY / self.gridSize) - self.dragOffsetGridY)

            if container.gridX != snapGridX or container.gridY != snapGridY:
                container.gridX = snapGridX
                container.gridY = snapGridY
                self.renderAll()

    def onRelease(self, event):
        if self.draggingWaypoint:
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
        self.connectingMousePos = (mx, my)
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


if __name__ == "__main__":
    app = NodeEditor()
    app.mainloop()