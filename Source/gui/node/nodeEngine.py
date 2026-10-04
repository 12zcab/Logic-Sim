import math
from tkinter import *
from typing import Dict, List, Tuple, Optional, Any
import xml.etree.ElementTree as ET
import re


def rotatePoint(x: float, y: float, cx: float, cy: float, angle_deg: float) -> Tuple[float, float]:
    """Rotate a point (x, y) around a center point (cx, cy) by angle_deg degrees."""
    if angle_deg % 360 == 0:
        return x, y
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    nx = cx + (x - cx) * cos_a - (y - cy) * sin_a
    ny = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return nx, ny


class ChildrenModel:
    def __init__(self, name: str, grid_x: float, grid_y: float, grid_w: float, grid_h: float,
                 svg_data: str = ""):
        self.name = name
        self.gridX = float(grid_x)
        self.gridY = float(grid_y)
        self.gridW = float(grid_w)
        self.gridH = float(grid_h)
        self.svg_data = svg_data
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
                 bg_color: str = "#2D3748", border_color: str = "#4A5568", angle: float = 0.0):
        self.parent = parent_editor
        self.name = name
        self.gridX = float(grid_x)
        self.gridY = float(grid_y)
        self.gridW = float(grid_w)
        self.gridH = float(grid_h)
        self.angle = angle
        self.bg_color = bg_color
        self.border_color = border_color
        self.canvasId = None
        self.nodes: Dict[str, NodeModel] = {}
        self.children: Dict[str, ChildrenModel] = {}

    def addNode(self, name: str, gridX: int, gridY: int, bg_color: str = "#1A202C", border_color: str = "#A0AEC0") -> NodeModel:
        node = NodeModel(name, gridX, gridY, bg_color=bg_color, border_color=border_color)
        self.nodes[name] = node
        if hasattr(self.parent, "nodeScaleAnim"):
            self.parent.nodeScaleAnim[(self, name)] = 0.6
        return node

    def addChild(self, name: str, gridX: float, gridY: float, gridW: float, gridH: float,
                 svg_data: str = "") -> ChildrenModel:
        child = ChildrenModel(name, gridX, gridY, gridW, gridH, svg_data=svg_data)
        self.children[name] = child
        return child


Container = ContainerModel
Node = NodeModel
Children = ChildrenModel


class NodeEditor(Frame):
    def __init__(self, master=None):
        super().__init__(master)

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

        self.canvas.focus_set()
        self.master.bind("<Key-r>", self.rotateSelectedContainer)
        self.master.bind("<Key-R>", self.rotateSelectedContainer)

        self.zoom = 1.0
        self.panX = 0.0
        self.panY = 0.0
        self.gridSize = 20

        self.containers: List[ContainerModel] = []
        self.connections: List[Dict[str, Any]] = []
        self.selectedContainer: Optional[ContainerModel] = None
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

    def rotateSelectedContainer(self, event=None):
        if self.selectedContainer:
            self.selectedContainer.angle = (self.selectedContainer.angle + 90) % 360
            self.renderAll()

    def sanitize_color(self, color: str) -> str:
        if not color:
            return ""
        if color.startswith("#") and len(color) == 9:
            alpha = color[7:9]
            if alpha.lower() == "00":
                return ""
            return color[:7]
        return color

    def addContainer(self, name: str, gridX: float, gridY: float, gridW: float, gridH: float,
                     bg_color: str = "#2D3748", border_color: str = "#4A5568", angle: float = 0.0) -> ContainerModel:
        container = ContainerModel(self, name, gridX, gridY, gridW, gridH, bg_color, border_color, angle)
        self.containers.append(container)
        return container

    def addConnection(self, fromContainer: ContainerModel, fromNode: str, toContainer: ContainerModel, toNode: str, waypoints: Optional[List[Tuple[float, float]]] = None):
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

    def getNodeCenterWindowSpace(self, container: ContainerModel, nName: str) -> Tuple[float, float]:
        logX, logY = self.getNodeCenterLogicalSpace(container, nName)
        return self.toWindowSpace(logX, logY)

    def getNodeCenterLogicalSpace(self, container: ContainerModel, nName: str) -> Tuple[float, float]:
        node = container.nodes[nName]
        unrotated_x = (container.gridX + node.gridX + 0.5) * self.gridSize
        unrotated_y = (container.gridY + node.gridY + 0.5) * self.gridSize

        center_x = (container.gridX + container.gridW / 2) * self.gridSize
        center_y = (container.gridY + container.gridH / 2) * self.gridSize

        return rotatePoint(unrotated_x, unrotated_y, center_x, center_y, container.angle)

    def findContainerAtPosition(self, logX: float, logY: float) -> Optional[ContainerModel]:
        for container in reversed(self.containers):
            cx = (container.gridX + container.gridW / 2) * self.gridSize
            cy = (container.gridY + container.gridH / 2) * self.gridSize
            
            # Unrotate click point back into container coordinate system
            rx, ry = rotatePoint(logX, logY, cx, cy, -container.angle)
            
            x0 = container.gridX * self.gridSize
            y0 = container.gridY * self.gridSize
            x1 = x0 + container.gridW * self.gridSize
            y1 = y0 + container.gridH * self.gridSize

            if x0 <= rx <= x1 and y0 <= ry <= y1:
                return container
        return None

    def findNodeAtPosition(self, winX: float, winY: float, maxDistance: float = 10):
        for container in self.containers:
            for nName in container.nodes:
                nx, ny = self.getNodeCenterWindowSpace(container, nName)
                dist = math.hypot(winX - nx, winY - ny)
                if dist <= maxDistance * self.zoom:
                    return (container, nName)
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
            startLog = self.getNodeCenterLogicalSpace(fromC, fromN)

            def checkBranchSegments(startPoint, branch):
                pts = [startPoint] + branch["waypoints"]
                if "to" in branch:
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

    def renderSvgData(self, svg_str: str, wx0: float, wy0: float, width: float, height: float, tags: Any, angle: float = 0.0, center_win: Tuple[float, float] = (0, 0)):
        def sanitize_color(color_str: str) -> str:
            if not color_str or color_str.lower() in ("none", "transparent"):
                return ""
            color_str = color_str.strip()
            if color_str.startswith("#") and len(color_str) == 9:
                alpha = color_str[7:9]
                if alpha.lower() == "00":
                    return ""
                return color_str[:7]
            if color_str.startswith("#") and len(color_str) == 5:
                r, g, b, a = color_str[1], color_str[2], color_str[3], color_str[4]
                if a == "0":
                    return ""
                return f"#{r}{r}{g}{g}{b}{b}"
            rgba_match = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)', color_str, re.IGNORECASE)
            if rgba_match:
                r, g, b = map(int, rgba_match.groups()[:3])
                a = float(rgba_match.group(4)) if rgba_match.group(4) is not None else 1.0
                if a == 0:
                    return ""
                return f"#{r:02x}{g:02x}{b:02x}"
            return color_str

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

        def transform_pt(x_val, y_val):
            wx = wx0 + (float(x_val) - vx) * scale_x
            wy = wy0 + (float(y_val) - vy) * scale_y
            if angle != 0:
                return rotatePoint(wx, wy, center_win[0], center_win[1], angle)
            return wx, wy

        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            fill = elem.attrib.get("fill", "none")
            stroke = elem.attrib.get("stroke", "none")
            sw_str = elem.attrib.get("stroke-width", "1")
            try:
                sw = float(sw_str) * min(scale_x, scale_y)
            except ValueError:
                sw = 1.0

            fill_val = sanitize_color(fill)
            stroke_val = sanitize_color(stroke)

            if tag == "rect":
                rx0 = float(elem.attrib.get("x", 0))
                ry0 = float(elem.attrib.get("y", 0))
                rw = float(elem.attrib.get("width", 0))
                rh = float(elem.attrib.get("height", 0))

                poly = [
                    transform_pt(rx0, ry0),
                    transform_pt(rx0 + rw, ry0),
                    transform_pt(rx0 + rw, ry0 + rh),
                    transform_pt(rx0, ry0 + rh)
                ]
                flat_pts = [c for pt in poly for c in pt]
                self.canvas.create_polygon(flat_pts, fill=fill_val, outline=stroke_val, width=sw, tags=tags)

            elif tag in ("circle", "ellipse"):
                cx_v = float(elem.attrib.get("cx", 0))
                cy_v = float(elem.attrib.get("cy", 0))
                rx_v = float(elem.attrib.get("r", elem.attrib.get("rx", 0)))
                ry_v = float(elem.attrib.get("r", elem.attrib.get("ry", 0)))

                steps = 16
                pts = []
                for i in range(steps):
                    a = math.radians(i * 360 / steps)
                    px = cx_v + rx_v * math.cos(a)
                    py = cy_v + ry_v * math.sin(a)
                    pts.extend(transform_pt(px, py))
                self.canvas.create_polygon(pts, fill=fill_val, outline=stroke_val, width=sw, smooth=True, tags=tags)

            elif tag == "line":
                p1 = transform_pt(elem.attrib.get("x1", 0), elem.attrib.get("y1", 0))
                p2 = transform_pt(elem.attrib.get("x2", 0), elem.attrib.get("y2", 0))
                self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=stroke_val if stroke_val else "#FFFFFF", width=sw, tags=tags)

            elif tag in ("polyline", "polygon"):
                pts_raw = elem.attrib.get("points", "").strip().split()
                pts = []
                for p in pts_raw:
                    coords = p.split(",")
                    if len(coords) == 2:
                        pts.extend(transform_pt(coords[0], coords[1]))
                if pts:
                    if tag == "polygon":
                        self.canvas.create_polygon(pts, fill=fill_val, outline=stroke_val, width=sw, tags=tags)
                    else:
                        self.canvas.create_line(pts, fill=stroke_val if stroke_val else "#FFFFFF", width=sw, tags=tags)

            elif tag == "path":
                d = elem.attrib.get("d", "")
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
                            pts.extend(transform_pt(cmd_list[idx], cmd_list[idx+1]))
                            idx += 2
                    else:
                        pts.extend(transform_pt(cmd_list[idx], cmd_list[idx+1]))
                        idx += 2
                if pts:
                    if fill_val:
                        self.canvas.create_polygon(pts, fill=fill_val, outline=stroke_val, width=sw, tags=tags)
                    else:
                        self.canvas.create_line(pts, fill=stroke_val if stroke_val else "#FFFFFF", width=sw, tags=tags)

    def createRoundedRectPoints(self, x0, y0, x1, y1, radius, angle=0.0, center=None):
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
                px = cx + radius * math.cos(rad)
                py = cy - radius * math.sin(rad)
                if angle != 0 and center:
                    px, py = rotatePoint(px, py, center[0], center[1], angle)
                points.extend([px, py])
        return points

    def drawRoundedRect(self, x0, y0, x1, y1, radius, fill, outline, width=2, tags="container", angle=0.0, center=None):
        points = self.createRoundedRectPoints(x0, y0, x1, y1, radius, angle=angle, center=center)
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

                if "to" in branch:
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

        for container in self.containers:
            cLogX = container.gridX * self.gridSize
            cLogY = container.gridY * self.gridSize
            cLogW = container.gridW * self.gridSize
            cLogH = container.gridH * self.gridSize

            wx0, wy0 = self.toWindowSpace(cLogX, cLogY)
            wx1, wy1 = self.toWindowSpace(cLogX + cLogW, cLogY + cLogH)

            centerLogX = (container.gridX + container.gridW / 2) * self.gridSize
            centerLogY = (container.gridY + container.gridH / 2) * self.gridSize
            centerWin = self.toWindowSpace(centerLogX, centerLogY)

            isSelected = container is self.selectedContainer

            container.canvasId = self.drawRoundedRect(
                wx0, wy0, wx1, wy1,
                radius=cornerRadiusPixels,
                fill=container.bg_color,
                outline=container.border_color if not isSelected else "#FFFFFF",
                width=borderWidth,
                tags=("container",),
                angle=container.angle,
                center=centerWin
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

                if child.svg_data:
                    self.renderSvgData(child.svg_data, chWx0, chWy0, w_px, h_px, tags=("child_svg",), angle=container.angle, center_win=centerWin)

            for nName, node in container.nodes.items():
                nodeKey = (container, nName)
                currentScale = self.nodeScaleAnim.get(nodeKey, 0.6)

                scaledSize = self.gridSize * currentScale
                offset = (self.gridSize - scaledSize) / 2

                nLogX = (container.gridX + node.gridX) * self.gridSize + offset
                nLogY = (container.gridY + node.gridY) * self.gridSize + offset

                nWx0, nWy0 = self.toWindowSpace(nLogX, nLogY)
                nWx1, nWy1 = self.toWindowSpace(nLogX + scaledSize, nLogY + scaledSize)

                pinRadius = (scaledSize * 0.25) * self.zoom
                isNodeHovered = (self.hoveredNode == (container, nName))

                if isNodeHovered or currentScale > 0.6:
                    glowPoints = self.createRoundedRectPoints(nWx0, nWy0, nWx1, nWy1, pinRadius, angle=container.angle, center=centerWin)
                    self.canvas.create_polygon(
                        glowPoints, fill="", outline="#FFFFFF", width=int(2 * self.zoom), smooth=True, tags="nodeGlow"
                    )

                node.canvasId = self.drawRoundedRect(
                    nWx0, nWy0, nWx1, nWy1,
                    radius=pinRadius,
                    fill=node.bg_color,
                    outline=node.border_color,
                    width=borderWidth,
                    tags=("node",),
                    angle=container.angle,
                    center=centerWin
                )

                nodeCenterLogX, nodeCenterLogY = self.getNodeCenterLogicalSpace(container, nName)
                textWinX, textWinY = self.toWindowSpace(nodeCenterLogX, nodeCenterLogY)

                scaledFontSize = int(4 * self.zoom * currentScale)

                self.canvas.create_text(
                    textWinX,
                    textWinY,
                    fill="white",
                    font=("Arial", scaledFontSize, "bold"),
                    text=node.name
                )

        self.canvas.tag_lower("connection")
        self.canvas.tag_lower("gridLine")

    def animateNodeScale(self, container: ContainerModel, nName: str, targetScale: float):
        nodeKey = (container, nName)

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

        for container in self.containers:
            for nName, node in container.nodes.items():
                nodeKey = (container, nName)
                targetScale = 1.0 if self.hoveredNode == (container, nName) else 0.6
                if self.nodeScaleAnim.get(nodeKey, 0.6) != targetScale:
                    self.animateNodeScale(container, nName, targetScale)

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
        self.canvas.focus_set()
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

        # Fix 2: Container detection works on unrotated and rotated geometric bounds (including over SVG elements)
        mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)
        container = self.findContainerAtPosition(mouseLogX, mouseLogY)
        if container:
            self.selectedContainer = container
            self.dragOffsetGridX = (mouseLogX / self.gridSize) - container.gridX
            self.dragOffsetGridY = (mouseLogY / self.gridSize) - container.gridY
            self.selectedConnectionIndex = None
            self.renderAll()
            return

        self.selectedContainer = None
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

        if self.selectedContainer:
            mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)

            snapGridX = round((mouseLogX / self.gridSize) - self.dragOffsetGridX)
            snapGridY = round((mouseLogY / self.gridSize) - self.dragOffsetGridY)

            if self.selectedContainer.gridX != snapGridX or self.selectedContainer.gridY != snapGridY:
                self.selectedContainer.gridX = snapGridX
                self.selectedContainer.gridY = snapGridY
                self.renderAll()

    def onRelease(self, event):
        if self.draggingWaypoint:
            self.draggingWaypoint = None
        # Fix 2: Retain self.selectedContainer on release so 'R' rotation keypress works!
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
    root = Tk()
    root.title("Node Editor")
    root.geometry("900x650")

    app = NodeEditor(master=root)
    app.pack(fill=BOTH, expand=True)

    box1 = app.addContainer("Box1", gridX=3, gridY=2, gridW=3, gridH=3, bg_color="#2A394A", border_color="#00ADB5")
    box2 = app.addContainer("Box1", gridX=-7, gridY=-3, gridW=3, gridH=3, bg_color="#342A4A", border_color="#BB86FC")

    box1.addNode("Pin0", -1, 0)
    box1.addNode("Pin1", -1, 2)
    box1.addNode("PinOut", 3, 1)
    box2.addNode("Pin0", -1, 1)
    box2.addNode("PinOut", 3, 1)

    sample_svg = '<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#00ADB5"/></svg>'
    try:
        with open("icon1.svg", "r") as f:
            sample_svg = f.read()
    except FileNotFoundError:
        pass

    box2.addChild("Hello", gridX=0, gridY=0, gridW=3, gridH=3, svg_data=sample_svg)
    app.addConnection(box1, "Pin0", box2, "PinOut")

    app.update_idletasks()
    app.renderAll()

    def toggle_activation():
        for connection in app.connections:
            connection["Activated"] = not connection.get("Activated", True)
        app.renderAll()
        root.after(1000, toggle_activation)

    root.after(1000, toggle_activation)
    root.mainloop()