bl_info = {
	"name": "Unity Batch Exporter",
	"description": "Exports selected objects as individual fbx files for Unity game engine.",
	"author": "Arda Hamamcıoğlu",
	"version": (1, 1),
	"support": "COMMUNITY",
	"category": "Import-Export"
}

import bpy
from bpy import context
import os

class UnityBatchExport(bpy.types.Operator):
	bl_idname = "object.unity_batch_export"
	bl_label = "Unity Batch Exporter"
	
	def execute(self,context):
		# export to blend file location
		basedir = os.path.dirname(bpy.data.filepath)
		exportdir = basedir+"/UnityExports"
		if not os.path.isdir(exportdir):
			os.mkdir(exportdir)

		if not exportdir:
			raise Exception("Blend file is not saved")

		scene = context.scene

		selection = context.selected_objects

		for obj in selection:

			name = bpy.path.clean_name(obj.name)
			fn = os.path.join(exportdir, name)
			bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
			bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, bake_space_transform=True, axis_forward="-Z",axis_up="Y",apply_scale_options="FBX_SCALE_ALL")

			print("written:", fn)

		return{'FINISHED'}

def menu_func(self,context):
   self.layout.operator(UnityBatchExport.bl_idname)

def register():
   bpy.utils.register_class(UnityBatchExport)
   bpy.types.TOPBAR_MT_fiappend(menu_func)

def unregister():
	bpy.utils.unregister_class(UnityBatchExport)
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
	register()