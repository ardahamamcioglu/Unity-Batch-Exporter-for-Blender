nbl_info = {
	"name": "Unity Batch Exporter",
	"description": "Exports objects directly into the unity project respecting collection hierarchy and ignore flags.",
	"author": "Arda Hamamcıoğlu",
	"version": (2, 0, 5),
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

class UnityExporterPanel(Panel):
	bl_idname = "OBJECT_PT_unity_export_panel"
	bl_label = "Unity Batch Export"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Unity Exporter"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		scn = context.scene

		row = layout.box()
		row.label(text="1)Select Unity Project Folder:")
		
		row.prop(scn, "project_path",icon ='FILE_IMAGE')
		
		row = layout.box()
		row.label(text="2)Hit The Button To Export:")
		
		row.operator("object.unity_batch_export")
		
		row = layout.row()
		row.label(text="Add * in Collection name to ignore.")

class UnityBatchExport(Operator):
	bl_idname = "object.unity_batch_export"
	bl_label = "Unity Batch Exporter"
	projectPath = ""

	def execute(self,context):
		scene = context.scene
		viewLayer = context.view_layer
		collections = scene.collection.children

		projectdir = bpy.path.abspath(scene.project_path)

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
			
			if len(collection.objects)==0 or "*" in collection.name:
				collectionPath = collectionPath.replace("*","")
				print(collectionPath)
				
				if os.path.isdir(collectionPath):
					shutil.rmtree(collectionPath)
					
			else:
				if not os.path.isdir(collectionPath):
					os.mkdir(collectionPath)
					
				for obj in collection.objects:
					obj.select_set(True)
					name = obj.name
					fn = os.path.join(collectionPath,name)
					bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
					bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, bake_space_transform=True,axis_forward="-Z",axis_up="Y",apply_scale_options="FBX_SCALE_ALL",check_existing=True,filter_glob="*.fbx",bake_anim=True,armature_nodetype='NULL',bake_anim_use_all_actions=True,embed_textures=False,object_types={'MESH'})
					obj.select_set(False)
					print("written:", fn)
			
		return{'FINISHED'}

def register():
	bpy.utils.register_class(UnityExporterPanel)
	bpy.utils.register_class(UnityBatchExport)
	bpy.types.Scene.project_path = bpy.props.StringProperty(name="Project Path", default = "", description = "Navigate to the Unity project file.", subtype = 'DIR_PATH')

def unregister():
	bpy.utils.unregister_class(UnityExporterPanel)
	bpy.utils.unregister_class(UnityBatchExport)
	del bpy.types.Scene.project_path

if __name__ == "__main__":
	register()