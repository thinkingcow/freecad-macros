import FreeCAD as App
import FreeCADGui as Gui
import Part
import math

# Cross-compatibility for FreeCAD UI
try:
    from PySide6 import QtWidgets, QtCore
except ImportError:
    try:
        from PySide2 import QtWidgets, QtCore
    except ImportError:
        from PySide import QtWidgets, QtCore


class ParametricSpiral:
    def __init__(self, obj, dia, turns, fill, prox, thick):
        obj.addProperty("App::PropertyLength", "Diameter", "Spiral Parameters", "Outside diameter of the spiral")
        obj.addProperty("App::PropertyFloat", "Turns", "Spiral Parameters", "Number of turns")
        obj.addProperty("App::PropertyFloat", "FillPercent", "Spiral Parameters", "Percent of fill (1.0 to 99.9)")
        obj.addProperty("App::PropertyFloat", "CenterProximity", "Spiral Parameters", "How close to center it begins (100% = center, 50% = halfway)")
        obj.addProperty("App::PropertyLength", "Thickness", "Spiral Parameters", "Extrusion thickness")
        
        obj.Diameter = dia
        obj.Turns = turns
        obj.FillPercent = fill
        obj.CenterProximity = prox
        obj.Thickness = thick
        obj.Proxy = self

    def dumps(self):
        return None

    def loads(self, state):
        return None

    def execute(self, fp):
        diameter = fp.Diameter
        turns = fp.Turns
        fill_pct = fp.FillPercent
        prox = fp.CenterProximity
        thickness = fp.Thickness

        if turns < 0.1: turns = 0.1
        if fill_pct <= 0: fill_pct = 0.1
        if fill_pct >= 100.0: fill_pct = 99.9
        if diameter <= 0.1: diameter = 0.1
        if prox < 0.1: prox = 0.1
        if prox > 100.0: prox = 100.0

        R_out = diameter / 2.0
        R_start = R_out * (1.0 - prox / 100.0)
        Delta_R = R_out - R_start

        N = turns
        f = fill_pct / 100.0

        P = Delta_R / (N + f)
        W = f * P
        b = P / (2 * math.pi)

        points_in = []
        points_out = []

        steps_per_turn = 72
        total_steps = int(math.ceil(N * steps_per_turn))

        for i in range(total_steps + 1):
            if i == total_steps:
                theta = 2 * math.pi * N 
            else:
                theta = (i / float(total_steps)) * (2 * math.pi * N)

            r_in = R_start + b * theta
            r_out = R_start + W + b * theta

            points_in.append(App.Vector(r_in * math.cos(theta), r_in * math.sin(theta), 0))
            points_out.insert(0, App.Vector(r_out * math.cos(theta), r_out * math.sin(theta), 0))

        try:
            curve_in = Part.BSplineCurve()
            curve_in.interpolate(points_in)
            edge_in = curve_in.toShape()

            curve_out = Part.BSplineCurve()
            curve_out.interpolate(points_out)
            edge_out = curve_out.toShape()
        except Exception as e:
            App.Console.PrintError(f"Curve Interpolation failed: {str(e)}\n")
            return

        p_in_start = edge_in.Vertexes[0].Point
        p_in_end = edge_in.Vertexes[-1].Point
        p_out_start = edge_out.Vertexes[0].Point
        p_out_end = edge_out.Vertexes[-1].Point

        cap1 = Part.makeLine(p_in_end, p_out_start)
        cap2 = Part.makeLine(p_out_end, p_in_start)

        wire = Part.Wire([edge_in, cap1, edge_out, cap2])

        if not wire.isClosed():
            App.Console.PrintError("Error: Generated wire is not closed.\n")
            return

        face = Part.Face(wire)
        
        if thickness > 0:
            # Extrude in the NEGATIVE Z direction so the top surface of the spiral
            # stays locked at Z=0, allowing it to sit flush inside the pocketed face.
            solid = face.extrude(App.Vector(0, 0, -thickness))
            solid = solid.removeSplitter()
            fp.Shape = solid
        else:
            fp.Shape = face


class ViewProviderSpiral:
    def __init__(self, vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object

    def updateData(self, fp, prop):
        pass

    def getIcon(self):
        return ""

    def dumps(self):
        return None

    def loads(self, state):
        return None


class SpiralGeneratorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, target_name=None):
        super().__init__(parent)
        title = f"Inlay Spiral into {target_name}" if target_name else "Create Parametric Spiral"
        self.setWindowTitle(title)
        self.setModal(True)
        self.layout = QtWidgets.QFormLayout(self)

        self.dia_input = QtWidgets.QDoubleSpinBox()
        self.dia_input.setRange(1.0, 10000.0)
        self.dia_input.setDecimals(2)
        self.dia_input.setValue(100.0)
        self.dia_input.setSuffix(" mm")
        self.layout.addRow("Outside Diameter:", self.dia_input)

        self.turns_input = QtWidgets.QDoubleSpinBox()
        self.turns_input.setRange(0.25, 1000.0)
        self.turns_input.setDecimals(2)
        self.turns_input.setValue(5.0)
        self.layout.addRow("Number of Turns:", self.turns_input)

        self.fill_input = QtWidgets.QDoubleSpinBox()
        self.fill_input.setRange(1.0, 99.9) 
        self.fill_input.setDecimals(1)
        self.fill_input.setValue(50.0)
        self.fill_input.setSuffix(" %")
        self.layout.addRow("Percent of Fill (Width):", self.fill_input)
        
        self.prox_input = QtWidgets.QDoubleSpinBox()
        self.prox_input.setRange(0.1, 100.0) 
        self.prox_input.setDecimals(1)
        self.prox_input.setValue(100.0)
        self.prox_input.setSuffix(" %")
        self.layout.addRow("Center Proximity:", self.prox_input)

        self.thick_input = QtWidgets.QDoubleSpinBox()
        self.thick_input.setRange(0.01, 10000.0)
        self.thick_input.setDecimals(2)
        self.thick_input.setValue(10.0)
        self.thick_input.setSuffix(" mm")
        self.layout.addRow("Extruded Thickness:", self.thick_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)


def create_parametric_spiral(dia, turns, fill, prox, thick, target_obj, target_face):
    doc = App.activeDocument()
    if doc is None:
        doc = App.newDocument()

    # Import this file as a module so FreeCAD serializes 'spiral.ParametricSpiral'
    # and 'spiral.ViewProviderSpiral' rather than '__main__.*'
    import spiral

    # Create the base spiral inlay solid
    spiral_obj = doc.addObject("Part::FeaturePython", "ExtrudedSpiral")
    spiral.ParametricSpiral(spiral_obj, dia, turns, fill, prox, thick)
    
    if App.GuiUp:
        spiral.ViewProviderSpiral(spiral_obj.ViewObject)

    cut = None
    # Handle Inlay / Boolean pocket logic if a target object and face are present
    if target_obj is not None and target_face is not None:
        try:
            # Determine face normal and center in global coordinates
            uv = target_face.Surface.parameter(target_face.CenterOfMass)
            normal = target_face.normalAt(uv[0], uv[1])
            center = target_face.CenterOfMass
            
            # Align the spiral's Z=0 top face flush with the target face
            placement = App.Placement()
            placement.Base = center
            placement.Rotation = App.Rotation(App.Vector(0, 0, 1), normal)
            spiral_obj.Placement = placement
            
            # Boolean subtraction to cut the matching pocket into the target object
            cut = doc.addObject("Part::Cut", f"{target_obj.Name}_Pocket")
            cut.Base = target_obj
            cut.Tool = spiral_obj
            
        except Exception as e:
            App.Console.PrintWarning(f"Failed to create Inlay pocket: {str(e)}\n")

    doc.recompute()

    # Restore visibility of BOTH the pocketed base object and the spiral inlay
    # so both separate solids can be exported together for multi-color 3D printing
    if App.GuiUp and cut is not None:
        target_obj.ViewObject.Visibility = False
        cut.ViewObject.Visibility = True
        spiral_obj.ViewObject.Visibility = True
        spiral_obj.ViewObject.ShapeColor = (1.0, 0.84, 0.0)

    if App.GuiUp:
        Gui.SendMsgToActiveView("ViewFit")


def run_macro():
    main_window = Gui.getMainWindow()
    
    # 1. Selection parsing logic (supports both Part objects and PartDesign Bodies)
    sel = Gui.Selection.getSelectionEx()
    target_obj = None
    target_face = None
    
    if len(sel) > 0:
        selection = sel[0]
        obj = selection.Object
        
        # If the user selected a sub-feature inside a PartDesign Body, target the Body
        if obj.TypeId != "PartDesign::Body" and hasattr(obj, "getParentGeoFeatureGroup"):
            parent_body = obj.getParentGeoFeatureGroup()
            if parent_body is not None and parent_body.TypeId == "PartDesign::Body":
                obj = parent_body
                
        if hasattr(obj, "Shape") and not obj.Shape.isNull():
            target_obj = obj
            
            # Check if the user explicitly clicked a single face
            if selection.HasSubObjects:
                for sub_obj in selection.SubObjects:
                    if isinstance(sub_obj, Part.Face):
                        target_face = sub_obj
                        break
            
            # If no explicit face was clicked, find the face pointing closest toward the camera
            if target_face is None and App.GuiUp:
                try:
                    view_dir = Gui.ActiveDocument.ActiveView.getViewDirection()
                    best_face = None
                    min_dist = float('inf')
                    
                    for f in target_obj.Shape.Faces:
                        try:
                            uv = f.Surface.parameter(f.CenterOfMass)
                            normal = f.normalAt(uv[0], uv[1])
                        except Exception:
                            continue
                            
                        # normal.dot(view_dir) < 0 means the face points toward the camera
                        if normal.dot(view_dir) < -1e-4:
                            dist = f.CenterOfMass.dot(view_dir)
                            if dist < min_dist:
                                min_dist = dist
                                best_face = f
                                
                    target_face = best_face
                except Exception as e:
                    App.Console.PrintWarning(f"Could not determine face from view: {str(e)}\n")
                    
    # 2. Trigger Dialog
    target_name = target_obj.Label if target_obj else None
    dialog = SpiralGeneratorDialog(main_window, target_name)
    
    exec_func = getattr(dialog, "exec", dialog.exec_)
    
    if exec_func() == QtWidgets.QDialog.Accepted:
        dia = dialog.dia_input.value()
        turns = dialog.turns_input.value()
        fill = dialog.fill_input.value()
        prox = dialog.prox_input.value()
        thick = dialog.thick_input.value()
        create_parametric_spiral(dia, turns, fill, prox, thick, target_obj, target_face)


if __name__ == "__main__":
    run_macro()
