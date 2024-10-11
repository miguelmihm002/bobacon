from typing import Optional, Sequence, Tuple

import gradio

import bobacon.choices
from bobacon import choices, face_detector, state_manager, wording
from bobacon.common_helper import calc_float_step, get_last
from bobacon.typing import Angle, FaceDetectorModel, Score
from bobacon.uis.core import register_ui_component
from bobacon.uis.typing import ComponentOptions

FACE_DETECTOR_MODEL_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_SIZE_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_ANGLES_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None
FACE_DETECTOR_SCORE_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global FACE_DETECTOR_MODEL_DROPDOWN
	global FACE_DETECTOR_SIZE_DROPDOWN
	global FACE_DETECTOR_ANGLES_CHECKBOX_GROUP
	global FACE_DETECTOR_SCORE_SLIDER

	face_detector_size_dropdown_options : ComponentOptions =\
	{
		'label': wording.get('uis.face_detector_size_dropdown'),
		'value': state_manager.get_item('face_detector_size')
	}
	if state_manager.get_item('face_detector_size') in bobacon.choices.face_detector_set[state_manager.get_item('face_detector_model')]:
		face_detector_size_dropdown_options['choices'] = bobacon.choices.face_detector_set[state_manager.get_item('face_detector_model')]
	with gradio.Row():
		FACE_DETECTOR_MODEL_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_detector_model_dropdown'),
			choices = bobacon.choices.face_detector_set.keys(),
			value = state_manager.get_item('face_detector_model')
		)
		FACE_DETECTOR_SIZE_DROPDOWN = gradio.Dropdown(**face_detector_size_dropdown_options)
	FACE_DETECTOR_ANGLES_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = wording.get('uis.face_detector_angles_checkbox_group'),
		choices = bobacon.choices.face_detector_angles,
		value = state_manager.get_item('face_detector_angles')
	)
	FACE_DETECTOR_SCORE_SLIDER = gradio.Slider(
		label = wording.get('uis.face_detector_score_slider'),
		value = state_manager.get_item('face_detector_score'),
		step = calc_float_step(bobacon.choices.face_detector_score_range),
		minimum = bobacon.choices.face_detector_score_range[0],
		maximum = bobacon.choices.face_detector_score_range[-1]
	)
	register_ui_component('face_detector_model_dropdown', FACE_DETECTOR_MODEL_DROPDOWN)
	register_ui_component('face_detector_size_dropdown', FACE_DETECTOR_SIZE_DROPDOWN)
	register_ui_component('face_detector_angles_checkbox_group', FACE_DETECTOR_ANGLES_CHECKBOX_GROUP)
	register_ui_component('face_detector_score_slider', FACE_DETECTOR_SCORE_SLIDER)


def listen() -> None:
	FACE_DETECTOR_MODEL_DROPDOWN.change(update_face_detector_model, inputs = FACE_DETECTOR_MODEL_DROPDOWN, outputs = [ FACE_DETECTOR_MODEL_DROPDOWN, FACE_DETECTOR_SIZE_DROPDOWN ])
	FACE_DETECTOR_SIZE_DROPDOWN.change(update_face_detector_size, inputs = FACE_DETECTOR_SIZE_DROPDOWN)
	FACE_DETECTOR_ANGLES_CHECKBOX_GROUP.change(update_face_detector_angles, inputs = FACE_DETECTOR_ANGLES_CHECKBOX_GROUP, outputs = FACE_DETECTOR_ANGLES_CHECKBOX_GROUP)
	FACE_DETECTOR_SCORE_SLIDER.release(update_face_detector_score, inputs = FACE_DETECTOR_SCORE_SLIDER)


def update_face_detector_model(face_detector_model : FaceDetectorModel) -> Tuple[gradio.Dropdown, gradio.Dropdown]:
	face_detector.clear_inference_pool()
	state_manager.set_item('face_detector_model', face_detector_model)

	if face_detector.pre_check():
		face_detector_size_choices = choices.face_detector_set.get(state_manager.get_item('face_detector_model'))
		state_manager.set_item('face_detector_size', get_last(face_detector_size_choices))
		return gradio.Dropdown(value = state_manager.get_item('face_detector_model')), gradio.Dropdown(value = state_manager.get_item('face_detector_size'), choices = face_detector_size_choices)
	return gradio.Dropdown(), gradio.Dropdown()


def update_face_detector_size(face_detector_size : str) -> None:
	state_manager.set_item('face_detector_size', face_detector_size)


def update_face_detector_angles(face_detector_angles : Sequence[Angle]) -> gradio.CheckboxGroup:
	face_detector_angles = face_detector_angles or bobacon.choices.face_detector_angles
	state_manager.set_item('face_detector_angles', face_detector_angles)
	return gradio.CheckboxGroup(value = state_manager.get_item('face_detector_angles'))


def update_face_detector_score(face_detector_score : Score) -> None:
	state_manager.set_item('face_detector_score', face_detector_score)