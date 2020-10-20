bl_info = {
"name": "Unity Batch Exporter",
"description": "Exports objects directly into the unity project respecting collection hierarchy and ignore flags.",
"author": "Arda Hamamcıoğlu",
"version": (2, 0, 81),
"blender" : (2, 90, 0),
"support": "COMMUNITY",
"category": "Import-Export"
}

import bpy
from bpy import context
from bpy.props import *
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

		row = layout.row()
		row.label(text="Add * in Collection name to ignore.")

class UnityBatchExport(Operator):
	bl_idname = "object.unity_batch_export"
	bl_label = "Unity Batch Exporter"

	def export_objects(objects,dir):
		
		bpy.ops.export_scene.fbx(
		filepath = dir,
		use_selection = True,
		use_active_collection = False,
		global_scale = 1.0,
		apply_unit_scale = True,
		apply_scale_options = 'FBX_SCALE_UNITS',
		bake_space_transform = True,
		object_types = {'MESH', 'ARMATURE', 'EMPTY', 'OTHER'},
		use_mesh_modifiers = True,
		use_mesh_modifiers_render = True,
		mesh_smooth_type = 'OFF',
		use_subsurf = False,
		use_mesh_edges = False,
		use_tspace = False,
		use_custom_props = False,
		add_leaf_bones = True,
		primary_bone_axis = 'Y',
		secondary_bone_axis = 'X',
		use_armature_deform_only = False,
		armature_nodetype = 'NULL',
		bake_anim = True,
		bake_anim_use_all_bones = True,
		bake_anim_use_nla_strips = True,
		bake_anim_use_all_actions = False,
		bake_anim_force_startend_keying = True,
		bake_anim_step = 1.0,
		bake_anim_simplify_factor = 1.0,
		path_mode = 'AUTO',
		embed_textures = False,
		batch_mode = 'OFF',
		use_batch_own_dir = True,
		axis_forward = '-Z',
		axis_up = 'Y'
		)
		print("Exported:", asset.name)
		asset.select_set(False)
	
	def execute(self,context):
		
		os.system("cls")
		scene = context.scene
		viewLayer = context.view_layer
		sceneCollection = bpy.context.scene.collection
		myprops = scene.my_props
 
        #Check if project path is entered.
		if myprops.project_path.strip():
			projectDir = bpy.path.abspath(myprops.project_path)
		else:
			raise Exception("No project path selected.")
        #Check if project path is valid
		if not os.path.isdir(projectDir):
			raise Exception("No project path is invalid.")

		exportDir = projectDir
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