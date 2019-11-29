bl_info = {
"name": "Unity Batch Exporter",
"description": "Exports objects directly into the unity project respecting collection hierarchy and ignore flags.",
"author": "Arda Hamamcıoğlu",
"version": (2, 0, 6),
"blender" : (2, 80, 0),
"support": "COMMUNITY",
"category": "Import-Export"
}

import bpy
from bpy import context
from bpy.props import (StringProperty,PointerProperty,BoolProperty,StringProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)
import os
import shutil

class MyProperties(bpy.types.PropertyGroup):
	sync_all : bpy.props.BoolProperty(name="Enable or Disable",description="A bool property",default = False)
	project_path : bpy.props.StringProperty(name="Project Path", default = "", description = "Navigate to the Unity project file.", subtype = 'DIR_PATH')

class UnityExporterPanel(Panel):
	bl_idname = "OBJECT_PT_unity_export_panel"
	bl_label = "Unity Batch Export"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Unity Exporter"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		myprops = context.scene.my_props

		row = layout.box()
		row.label(text="1)Select Unity Project Folder:")

		row.prop(myprops, "project_path",icon ='FILE_IMAGE')

		row = layout.box()
		row.label(text="2)Hit The Button To Export:")

		row.operator("object.unity_batch_export")

		row = layout.box()
		row.prop(myprops,"sync_all", text="Sync Deleted Files")

		row = layout.row()
		row.label(text="Add * in Collection name to ignore.")

class UnityBatchExport(Operator):
				bl_idname = "object.unity_batch_export"
				bl_label = "Unity Batch Exporter"

				def execute(self,context):
					scene = context.scene
					viewLayer = context.view_layer
					collectionLayer = bpy.context.view_layer.active_layer_collection
					myprops = scene.my_props

					bpy.ops.object.make_single_user(type='ALL', object=True, obdata=False, material=False, animation=False)
#Check if project path is entered.
					if myprops.project_path.strip():
						projectDir = bpy.path.abspath(myprops.project_path)
					else:
						raise Exception("No project path selected.")
#Check if project path is valid
					if not os.path.isdir(projectDir):
						raise Exception("No project path is invalid.")

					exportdir = projectDir +"Assets/Models"
#Check if Models folder exists in the project
					if not os.path.isdir(exportdir):
						os.makedirs(exportdir)

					bpy.ops.object.select_all(action='DESELECT')

					for collection in collectionLayer.children:
						if collection.is_visible:
							collection = collection.collection
							collectionPath = exportdir +"/" + collection.name

							if len(collection.objects)==0 or "*" in collection.name:
								collectionPath = collectionPath.replace("*","")

								if os.path.isdir(collectionPath) and scene.sync_all:
									shutil.rmtree(collectionPath)
							else:
								if not os.path.isdir(collectionPath):
									os.mkdir(collectionPath)

								for obj in collection.objects:
									obj.select_set(True)
									name = obj.name
									fn = os.path.join(collectionPath,name)
									bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
									bpy.context.object.hide_viewport = False
									bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, bake_space_transform=True,axis_forward="-Z",axis_up="Y",apply_scale_options="FBX_SCALE_ALL",check_existing=True,filter_glob="*.fbx",bake_anim=True,armature_nodetype='NULL',bake_anim_use_all_actions=True,embed_textures=False,object_types={'MESH'})
									obj.select_set(False)
									print("written:", fn)

					return{'FINISHED'}

classes = (MyProperties,UnityExporterPanel,UnityBatchExport)

def register():
	for c in classes:
		bpy.utils.register_class(c)
	bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MyProperties)

def unregister():
	for c in reversed(classes):
		bpy.utils.unregister_class(c)
	del bpy.types.Scene.my_props

if __name__ == "__main__":
	register()