import bpy
import time

# Define a custom property group for recording properties
class RecordingProperties(bpy.types.PropertyGroup):
    start_time: bpy.props.FloatProperty(
        name="Start Time",
        description="The time when the recording started",
        default=0.0,
    )

# Define the UI panel for the recording properties
class RecordingPropertiesPanel(bpy.types.Panel):
    bl_label = "Recording Properties"
    bl_idname = "VIEW3D_PT_recording_properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Recording"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def draw(self, context):
        layout = self.layout
        rec_props = context.scene.rec_props

        row = layout.row()
        row.label(text=f"Time since record start: {time.time() - rec_props.start_time:.2f} seconds")

        row = layout.row()
        row.operator("wm.start_recording")
        row.operator("wm.stop_recording")

class StartRecordingOperator(bpy.types.Operator):
    bl_idname = "wm.start_recording"
    bl_label = "Start Recording"

    def execute(self, context):
        context.scene.rec_props.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        self._timer = context.window_manager.event_timer_add(1.0, window=context.window)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'TIMER'}:
            return {'PASS_THROUGH'}
        return {'RUNNING_MODAL'}

class StopRecordingOperator(bpy.types.Operator):
    bl_idname = "wm.stop_recording"
    bl_label = "Stop Recording"

    def execute(self, context):
        context.window_manager.event_timer_remove(self._timer)
        return {'FINISHED'}

# Register and unregister functions
classes = (RecordingProperties, RecordingPropertiesPanel, StartRecordingOperator, StopRecordingOperator)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rec_props = bpy.props.PointerProperty(type=RecordingProperties)

def unregister():
    del bpy.types.Scene.rec_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
