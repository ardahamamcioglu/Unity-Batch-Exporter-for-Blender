bl_info = {
    "name": "Unity Batch Exporter",
    "description": "Exports selected objects as individual fbx files for Unity game engine.",
    "author": "Arda Hamamcıoğlu",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "support": "COMMUNITY",
    "category": "Import-Export"
}

import bpy
import os

class UnityBatchExport(bpy.types.Operator):
    bl_idname = "object.unity_batch_export"
    bl_label = "Export Selected Objects For Unity"
    
    def execute(self,context):
        # export to blend file location
        basedir = os.path.dirname(bpy.data.filepath)
        exportdir = basedir+"/UnityExports"
        if not os.path.isdir(exportdir):
            os.mkdir(exportdir)

        if not exportdir:
            raise Exception("Blend file is not saved")

        scene = bpy.context.scene

        obj_active = scene.objects.active
        selection = bpy.context.selected_objects

        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:

            obj.select = True

            # some exporters only use the active object
            scene.objects.active = obj

            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(exportdir, name)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, bake_space_transform=True, axis_forward="-Z",axis_up="Y",apply_scale_options="FBX_SCALE_ALL")
            obj.select = False

            print("written:", fn)

        scene.objects.active = obj_active

        for obj in selection:
            obj.select = True
        return{'FINISHED'}
def register():
	bpy.utils.register_class(UnityBatchExport)
def unregister():
	bpy.utils.unregister_class(UnityBatchExport)
