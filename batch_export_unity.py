bl_info = {
"name": "Unity Batch Exporter",
"description": "Exports objects directly into the unity project respecting collection hierarchy and ignore flags.",
"author": "Arda Hamamcıoğlu",
"version": (2, 0, 81),
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

				def get_parent_collection_names(collection, parent_names):
					for parent_collection in bpy.data.collections:
					   if collection.name in parent_collection.children.keys():
						   parent_names.append(parent_collection.name)
						   UnityBatchExport.get_parent_collection_names(parent_collection, parent_names)
						   return
				
				def turn_collection_hierarchy_into_path(obj):
					parent_collection = obj.users_collection[0]
					parent_names	  = []
					parent_names.append(parent_collection.name)
					UnityBatchExport.get_parent_collection_names(parent_collection, parent_names)
					parent_names.reverse()
					path = '/'.join(parent_names)
					if  '*' in path:
					   return ''
					else:
						return path

				def export_objects(objects,dir):
					for asset in objects:
						asset.select_set(True)

						collectionPath = UnityBatchExport.turn_collection_hierarchy_into_path(asset)
						print(collectionPath)
						if len(collectionPath.strip())!=0:
							exportPath = dir+'/'+collectionPath
							if not os.path.isdir(exportPath):
								os.makedirs(exportPath)
						
							name = asset.name
							fn = os.path.join(exportPath,name)
							bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
							bpy.context.object.hide_viewport = False
							bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, bake_space_transform=True,axis_forward="-Z",axis_up="Y",apply_scale_options="FBX_SCALE_ALL",check_existing=True,filter_glob="*.fbx",bake_anim=True,armature_nodetype='NULL',bake_anim_use_all_actions=True,embed_textures=False,object_types={'MESH'})
							print("Exported:", asset.name)
						asset.select_set(False)
				def execute(self,context):
					scene = context.scene
					viewLayer = context.view_layer
					sceneCollection = bpy.context.scene.collection
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

					exportDir = projectDir +"Assets/Models"
#Check if Models folder exists in the project
					if not os.path.isdir(exportDir):
						os.makedirs(exportDir)

					UnityBatchExport.export_objects(bpy.context.view_layer.objects,exportDir)
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