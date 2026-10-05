import math
import copy
from tkinter import *
from typing import Dict, List, Tuple, Optional, Any


def rotatePoint(x: float, y: float, cx: float, cy: float, angle_deg: float) -> Tuple[float, float]:
    if angle_deg % 360 == 0:
        return x, y
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    nx = cx + (x - cx) * cos_a - (y - cy) * sin_a
    ny = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return nx, ny


class ChildrenModel:
    def __init__(self, name: str, grid_x: float, grid_y: float, grid_w: float = 1.0, grid_h: float = 1.0,
                 python_script: str = ""):
        self.name = name
        self.gridX = float(grid_x)
        self.gridY = float(grid_y)
        self.gridW = float(grid_w)
        self.gridH = float(grid_h)
        self.python_script = python_script
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
    def __init__(self, parent_editor, name: str, grid_x: float, grid_y: float,
                 grid_w: float = 1.0, grid_h: float = 1.0,
                 bg_color: str = "#2D3748", border_color: str = "#4A5568", angle: float = 0.0):
        self.parent = parent_editor
        self.name = name
        self.gridX = float(grid_x)
        self.gridY = float(grid_y)
        self.gridW = float(grid_w)
        self.gridH = float(grid_h)
        self.angle = angle % 360
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

    def addChild(self, name: str, gridX: float, gridY: float, gridW: float = 1.0, gridH: float = 1.0,
                 python_script: str = "") -> ChildrenModel:
        child = ChildrenModel(name, gridX, gridY, gridW, gridH, python_script=python_script)
        self.children[name] = child
        return child


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

        self.master.bind_all("r", self.rotateSelectedContainer)
        self.master.bind_all("R", self.rotateSelectedContainer)

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

    def getContainerCenterLogical(self, container: ContainerModel) -> Tuple[float, float]:
        cx = (container.gridX + container.gridW / 2.0) * self.gridSize
        cy = (container.gridY + container.gridH / 2.0) * self.gridSize
        
        # Shift pivot by 0.5 units for odd/even mixed parities to align rotated nodes to grid centers
        if container.gridW % 2 != container.gridH % 2:
            if container.gridW % 2 == 0:
                cx += 0.5 * self.gridSize
            else:
                cy += 0.5 * self.gridSize
                
        return cx, cy

    def rotateSelectedContainer(self, event=None):
        if self.selectedContainer:
            self.selectedContainer.angle = (self.selectedContainer.angle + 90) % 360
            self.renderAll()

    def addContainer(self, name: str, gridX: float, gridY: float, gridW: float = 1.0, gridH: float = 1.0,
                     bg_color: str = "#2D3748", border_color: str = "#4A5568", angle: float = 0.0) -> ContainerModel:
        container = ContainerModel(self, name, gridX, gridY, gridW, gridH, bg_color=bg_color, border_color=border_color, angle=angle)
        self.containers.append(container)
        return container

    def deleteContainer(self, container: ContainerModel):
        if container in self.containers:
            self.containers.remove(container)
        if self.selectedContainer == container:
            self.selectedContainer = None

        # Clean up any connections attached to nodes in this container
        new_connections = []
        for conn in self.connections:
            fromC, _ = conn["from"]
            if fromC == container:
                continue

            def filterBranches(branches):
                valid_branches = []
                for b in branches:
                    if "to" in b:
                        toC, _ = b["to"]
                        if toC == container:
                            continue
                    b["sub_branches"] = filterBranches(b.get("sub_branches", []))
                    valid_branches.append(b)
                return valid_branches

            conn["branches"] = filterBranches(conn["branches"])
            if conn["branches"]:
                new_connections.append(conn)

        self.connections = new_connections

    def addConnection(self, from_container: ContainerModel, from_pin: str, to_container: ContainerModel, to_pin: str):
        conn = {
            "from": (from_container, from_pin),
            "branches": [
                {
                    "waypoints": [],
                    "to": (to_container, to_pin),
                    "sub_branches": []
                }
            ],
            "Activated": True
        }
        self.connections.append(conn)
        return conn

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
        center_x, center_y = self.getContainerCenterLogical(container)
        return rotatePoint(unrotated_x, unrotated_y, center_x, center_y, container.angle)

    def isPointInRotatedRect(self, winX: float, winY: float, container: ContainerModel) -> bool:
        logX, logY = self.toLogicalSpace(winX, winY)
        cx, cy = self.getContainerCenterLogical(container)
        unrotX, unrotY = rotatePoint(logX, logY, cx, cy, -container.angle)

        x0 = container.gridX * self.gridSize
        x1 = (container.gridX + container.gridW) * self.gridSize
        y0 = container.gridY * self.gridSize
        y1 = (container.gridY + container.gridH) * self.gridSize

        return (x0 <= unrotX <= x1) and (y0 <= unrotY <= y1)

    def findContainerAtWindowPos(self, winX: float, winY: float) -> Optional[ContainerModel]:
        # Collect all canvas tags under the mouse cursor
        items = self.canvas.find_overlapping(winX - 2, winY - 2, winX + 2, winY + 2)
        hit_tags = set()
        if items:
            for item in items:
                hit_tags.update(self.canvas.gettags(item))

        # Evaluate layers top-to-bottom so upper layers take priority over lower layers
        for container in reversed(self.containers):
            # 1. Check if mouse hits any child of THIS container
            for child in container.children.values():
                if f"child_{id(child)}" in hit_tags:
                    return container

            # 2. Check bounding box hit for THIS container (unless transparent)
            is_transparent = (
                container.bg_color in ("transparent", "", "none", None) and 
                container.border_color in ("transparent", "", "none", None)
            )
            
            if not is_transparent:
                if self.isPointInRotatedRect(winX, winY, container):
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

    def executePythonIconScript(self, child: ChildrenModel, wx0: float, wy0: float, width: float, height: float, tags: Any, angle: float = 0.0, center_win: Tuple[float, float] = (0, 0), is_selected: bool = False):
        if not child.python_script or width <= 0 or height <= 0:
            return

        def draw_oval(cx_circle, cy_circle, r, fill="", outline="#FFFFFF", width=2):
            if angle != 0:
                cx_circle, cy_circle = rotatePoint(cx_circle, cy_circle, center_win[0], center_win[1], angle)
            return self.canvas.create_oval(cx_circle - r, cy_circle - r, cx_circle + r, cy_circle + r,
                                           fill=fill, outline=outline, width=width, tags=tags)

        def draw_polygon(points, fill="", outline="#FFFFFF", width=2):
            rot_points = []
            for i in range(0, len(points), 2):
                px, py = points[i], points[i+1]
                if angle != 0:
                    px, py = rotatePoint(px, py, center_win[0], center_win[1], angle)
                rot_points.extend([px, py])
            return self.canvas.create_polygon(rot_points, fill=fill, outline=outline, width=width, tags=tags)

        def draw_rect(rx0, ry0, rx1, ry1, fill="", outline="#FFFFFF", width=2):
            rect_pts = [rx0, ry0, rx1, ry0, rx1, ry1, rx0, ry1]
            return draw_polygon(rect_pts, fill=fill, outline=outline, width=width)

        def draw_line(x1_l, y1_l, x2_l, y2_l, fill="#FFFFFF", width=2):
            if angle != 0:
                x1_l, y1_l = rotatePoint(x1_l, y1_l, center_win[0], center_win[1], angle)
                x2_l, y2_l = rotatePoint(x2_l, y2_l, center_win[0], center_win[1], angle)
            return self.canvas.create_line(x1_l, y1_l, x2_l, y2_l, fill=fill, width=width, tags=tags)

        scope = {
            "canvas": self.canvas,
            "x": wx0,
            "y": wy0,
            "w": width,
            "h": height,
            "tags": tags,
            "angle": angle,
            "cx": center_win[0],
            "cy": center_win[1],
            "is_selected": is_selected,
            "rotatePoint": rotatePoint,
            "draw_oval": draw_oval,
            "draw_polygon": draw_polygon,
            "draw_rect": draw_rect,
            "draw_line": draw_line,
            "math": math
        }

        try:
            exec(child.python_script, scope)
        except Exception as e:
            print(f"[PythonIconScript Execution Error] {e}")

    def createRoundedRectPoints(self, x0, y0, x1, y1, radius, angle=0.0, center=None):
        radius = max(1, min(radius, (x1 - x0) / 2.0, (y1 - y0) / 2.0))
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
        fill_val = "" if fill in ("transparent", "", "none", None) else fill
        outline_val = "" if outline in ("transparent", "", "none", None) else outline
        return self.canvas.create_polygon(points, fill=fill_val, outline=outline_val, width=width, tags=tags)

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

            centerLogX, centerLogY = self.getContainerCenterLogical(container)
            centerWin = self.toWindowSpace(centerLogX, centerLogY)

            isSelected = container is self.selectedContainer

            border_color = container.border_color
            if isSelected and container.border_color != "transparent":
                border_color = "#FFFFFF"

            container.canvasId = self.drawRoundedRect(
                wx0, wy0, wx1, wy1,
                radius=cornerRadiusPixels,
                fill=container.bg_color,
                outline=border_color,
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

                if child.python_script:
                    child_tag = f"child_{id(child)}"
                    self.executePythonIconScript(
                        child, chWx0, chWy0, w_px, h_px,
                        tags=("child_python_icon", child_tag),
                        angle=container.angle,
                        center_win=centerWin,
                        is_selected=isSelected
                    )

            for nName, node in container.nodes.items():
                nodeKey = (container, nName)
                currentScale = self.nodeScaleAnim.get(nodeKey, 0.6)

                scaledSize = self.gridSize * currentScale
                offset = (self.gridSize - scaledSize) / 2.0

                nLogX = (container.gridX + node.gridX) * self.gridSize + offset
                nLogY = (container.gridY + node.gridY) * self.gridSize + offset

                nWx0, nWy0 = self.toWindowSpace(nLogX, nLogY)
                nWx1, nWy1 = self.toWindowSpace(nLogX + scaledSize, nLogY + scaledSize)

                pinRadius = (scaledSize * 0.25) * self.zoom
                isNodeHovered = (self.hoveredNode == (container, nName))

                if isNodeHovered or currentScale > 0.6:
                    glowPoints = self.createRoundedRectPoints(nWx0, nWy0, nWx1, nWy1, pinRadius, angle=container.angle, center=centerWin)
                    self.canvas.create_polygon(
                        glowPoints, fill="", outline="#FFFFFF", width=int(2 * self.zoom), tags="nodeGlow"
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

                if scaledFontSize > 0:
                    self.canvas.create_text(
                        textWinX,
                        textWinY,
                        fill="white",
                        font=("Arial", scaledFontSize, "bold"),
                        text=node.name,
                        tags="node"
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
            return

        container = self.findContainerAtWindowPos(event.x, event.y)
        if container:
            self.deleteContainer(container)
            self.renderAll()
            return

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

        container = self.findContainerAtWindowPos(event.x, event.y)
        if container:
            mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)
            self.selectedContainer = container
            self.dragOffsetGridX = (mouseLogX / self.gridSize) - container.gridX
            self.dragOffsetGridY = (mouseLogY / self.gridSize) - container.gridY
            self.selectedConnectionIndex = None

            # Bring selected container to top of layer stack
            if container in self.containers:
                self.containers.remove(container)
                self.containers.append(container)

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
            newGridX = math.floor((mouseLogX / self.gridSize) - self.dragOffsetGridX)
            newGridY = math.floor((mouseLogY / self.gridSize) - self.dragOffsetGridY)
            self.selectedContainer.gridX = newGridX
            self.selectedContainer.gridY = newGridY
            self.renderAll()

    def onRelease(self, event):
        self.draggingWaypoint = None

    def onMouseWheel(self, event):
        if event.num == 4 or event.delta > 0:
            zoom_factor = 1.1
        else:
            zoom_factor = 0.9

        # Capture mouse position in logical space prior to zoom scaling
        mouseLogX, mouseLogY = self.toLogicalSpace(event.x, event.y)

        self.zoom *= zoom_factor

        # Adjust panning offsets so the logical coordinate stays fixed under the cursor
        cx, cy, _, _ = self.getCenter()
        self.panX = event.x - cx - (mouseLogX * self.zoom)
        self.panY = event.y - cy - (mouseLogY * self.zoom)

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
    root.geometry("1000x700")

    editor = NodeEditor(root)
    editor.pack(fill=BOTH, expand=True)

    c1 = editor.addContainer("Container 1", gridX=-2, gridY=-2, gridW=3, gridH=2, bg_color="#2D3748")
    c1.addNode("A", 0, 0)
    c1.addNode("B", 2, 1)

    c2 = editor.addContainer("Transparent Container", gridX=3, gridY=1, gridW=3, gridH=2, bg_color="transparent", border_color="transparent")
    c2.addNode("C", 0, 0)
    
    script = """
draw_rect(x + 5, y + 5, x + w - 5, y + h - 5, fill="#4A5568", outline="#A0AEC0")
"""
    c2.addChild("Icon", 1.0, 0.5, 1.0, 1.0, python_script=script)

    editor.renderAll()
    root.mainloop()