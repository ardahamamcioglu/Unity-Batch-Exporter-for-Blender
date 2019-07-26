bl_info = {
	"name": "Unity Batch Exporter",
	"description": "Exports objects directly into the unity project respecting collection hierarchy and ignore flags.",
	"author": "Arda Hamamcıoğlu",
<<<<<<< Updated upstream
	"version": (2, 0),
=======
	"version": (1, 9 ,1),
>>>>>>> Stashed changes
   "blender" : (2, 80, 0),
	"support": "COMMUNITY",
	"category": "Import-Export"
}

import bpy
from bpy import context
from bpy.props import (StringProperty,
					   PointerProperty,
					   )
from bpy.types import (Panel,
					   Operator,
					   AddonPreferences,
					   PropertyGroup,
					   )
import os
import shutil

<<<<<<< Updated upstream
class ImportSettings(PropertyGroup):

	path = StringProperty(name="",description="Path to Directory",default="",maxlen=1024,subtype='DIR_PATH')

class UnityExporterPanel(bpy.types.Panel):
	bl_label = "Unity Exporter"
	bl_idname = "OBJECT_PT_unityExport"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "output"

	def draw(self, context):
		layout = self.layout

		obj = context.object

		row = layout.row()
		row.prop(bpy.ops.object.unity_batch_exporter,"projectPath",text="")
		
		row = layout.row()
		row.operator("object.unity_batch_export")

		print(bpy.ops.object.unity_batch_exporter.projectPath)


class UnityBatchExport(bpy.types.Operator):
=======
class UnityExporterPanel(Panel):
	bl_idname = "OBJECT_PT_my_panel"
	bl_label = "My Tool"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Unity Exporter"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		
		
		row = layout.box()
		row.label(text="1)Select Unity Project File:")
		
		row.prop(scn, "project_path",icon ='FILE_IMAGE')
		
		row = layout.box()
		row.label(text="2)Select Unity Project File:")
		
		row.operator("object.unity_batch_export")
		
		row = layout.row()
		row.label(text="Add * in Collection name to ignore.")
		
class UnityBatchExport(Operator):
>>>>>>> Stashed changes
	bl_idname = "object.unity_batch_export"
	bl_label = "Unity Batch Exporter"
	projectPath = ""

	def execute(self,context):
		scene = context.scene
		selection = context.selected_objects
		collections = bpy.context.scene.collection.children 
		
		if len(selection) == 0:
			raise Exception("No Object Selected to Export")
		# export to blend file location
		basedir = os.path.dirname(bpy.data.filepath)
		projectdir = scene.project_path

		if not os.path.isdir(projectdir):
			raise Exception("No project path selected.")
		
		exportdir = projectdir +"Assets/Models"
		
		if not os.path.isdir(exportdir):
			os.makedirs(exportdir)
		if not exportdir:
			raise Exception("Blend file has not been not saved yet.")
		
		bpy.ops.object.select_all(action='DESELECT')
		
		
		for collection in collections:
			collectionPath = exportdir +"/" + collection.name
			if collection.all_objects == 0 or "*" in collection.name:
				collectionPath = collectionPath.replace("*","")
				print(collectionPath)
				if os.path.isdir(collectionPath):
					shutil.rmtree(collectionPath)
			else:
				if not os.path.isdir(collectionPath):
					os.mkdir(collectionPath)
				for obj in collection.all_objects:
					if obj.type in ["MESH"]:
						name = bpy.path.clean_name(obj.name)
						fn = os.path.join(collectionPath,name)
						bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
						bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, bake_space_transform=True, axis_forward="-Z",axis_up="Y",apply_scale_options="FBX_SCALE_ALL")
						print("written:", fn)
			
		return{'FINISHED'}

#def menu_func(self,context):
#   self.layout.operator(UnityBatchExport.bl_idname)

def register():
	bpy.utils.register_class(UnityExporterPanel)
	bpy.utils.register_class(UnityBatchExport)
<<<<<<< Updated upstream
	bpy.types.TOPBAR_MT_file_export.append(menu_func)
	bpy.utils.register_module(__name__)
	bpy.ops.object.unity_batch_exporter = PointerProperty(type=ImportSettings)
	
=======
	bpy.types.Scene.project_path = bpy.props.StringProperty(name="Project Path", default = "", description = "Navigate to the Unity project file.", subtype = 'FILE_PATH')
#   bpy.types.TOPBAR_MT_file_export.append(menu_func)
>>>>>>> Stashed changes

def unregister():
	bpy.utils.unregister_class(UnityExporterPanel)
	bpy.utils.unregister_class(UnityBatchExport)
<<<<<<< Updated upstream
	bpy.utils.unregister_class(UnityExporterPanel)
	bpy.utils.unregister_module(__name__)
	del bpy.ops.object.unity_batch_exporter
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
=======
	del bpy.types.Scene.project_path
>>>>>>> Stashed changes

if __name__ == "__main__":
	register()