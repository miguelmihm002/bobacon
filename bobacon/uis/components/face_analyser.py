from typing import Optional, Dict, Any, Tuple

import gradio

import bobacon.globals
import bobacon.choices
from bobacon import face_analyser, wording
from bobacon.typing import FaceAnalyserOrder, FaceAnalyserAge, FaceAnalyserGender, FaceDetectorModel
from bobacon.uis.core import register_ui_component

FACE_ANALYSER_ORDER_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_ANALYSER_AGE_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_ANALYSER_GENDER_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_MODEL_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_SIZE_DROPDOWN : Optional[gradio.Dropdown] = None
FACE_DETECTOR_SCORE_SLIDER : Optional[gradio.Slider] = None
FACE_LANDMARKER_SCORE_SLIDER : Optional[gradio.Slider] = None


def render() -> None:
	global FACE_ANALYSER_ORDER_DROPDOWN
	global FACE_ANALYSER_AGE_DROPDOWN
	global FACE_ANALYSER_GENDER_DROPDOWN
	global FACE_DETECTOR_MODEL_DROPDOWN
	global FACE_DETECTOR_SIZE_DROPDOWN
	global FACE_DETECTOR_SCORE_SLIDER
	global FACE_LANDMARKER_SCORE_SLIDER

	face_detector_size_dropdown_args : Dict[str, Any] =\
	{
		'label': wording.get('uis.face_detector_size_dropdown'),
		'value': bobacon.globals.face_detector_size
	}
	if bobacon.globals.face_detector_size in bobacon.choices.face_detector_set[bobacon.globals.face_detector_model]:
		face_detector_size_dropdown_args['choices'] = bobacon.choices.face_detector_set[bobacon.globals.face_detector_model]
	with gradio.Row():
		FACE_ANALYSER_ORDER_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_analyser_order_dropdown'),
			choices = bobacon.choices.face_analyser_orders,
			value = bobacon.globals.face_analyser_order
		)
		FACE_ANALYSER_AGE_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_analyser_age_dropdown'),
			choices = [ 'none' ] + bobacon.choices.face_analyser_ages,
			value = bobacon.globals.face_analyser_age or 'none'
		)
		FACE_ANALYSER_GENDER_DROPDOWN = gradio.Dropdown(
			label = wording.get('uis.face_analyser_gender_dropdown'),
			choices = [ 'none' ] + bobacon.choices.face_analyser_genders,
			value = bobacon.globals.face_analyser_gender or 'none'
		)
	FACE_DETECTOR_MODEL_DROPDOWN = gradio.Dropdown(
		label = wording.get('uis.face_detector_model_dropdown'),
		choices = bobacon.choices.face_detector_set.keys(),
		value = bobacon.globals.face_detector_model
	)
	FACE_DETECTOR_SIZE_DROPDOWN = gradio.Dropdown(**face_detector_size_dropdown_args)
	with gradio.Row():
		FACE_DETECTOR_SCORE_SLIDER = gradio.Slider(
			label = wording.get('uis.face_detector_score_slider'),
			value = bobacon.globals.face_detector_score,
			step = bobacon.choices.face_detector_score_range[1] - bobacon.choices.face_detector_score_range[0],
			minimum = bobacon.choices.face_detector_score_range[0],
			maximum = bobacon.choices.face_detector_score_range[-1]
		)
		FACE_LANDMARKER_SCORE_SLIDER = gradio.Slider(
			label = wording.get('uis.face_landmarker_score_slider'),
			value = bobacon.globals.face_landmarker_score,
			step = bobacon.choices.face_landmarker_score_range[1] - bobacon.choices.face_landmarker_score_range[0],
			minimum = bobacon.choices.face_landmarker_score_range[0],
			maximum = bobacon.choices.face_landmarker_score_range[-1]
		)
	register_ui_component('face_analyser_order_dropdown', FACE_ANALYSER_ORDER_DROPDOWN)
	register_ui_component('face_analyser_age_dropdown', FACE_ANALYSER_AGE_DROPDOWN)
	register_ui_component('face_analyser_gender_dropdown', FACE_ANALYSER_GENDER_DROPDOWN)
	register_ui_component('face_detector_model_dropdown', FACE_DETECTOR_MODEL_DROPDOWN)
	register_ui_component('face_detector_size_dropdown', FACE_DETECTOR_SIZE_DROPDOWN)
	register_ui_component('face_detector_score_slider', FACE_DETECTOR_SCORE_SLIDER)
	register_ui_component('face_landmarker_score_slider', FACE_LANDMARKER_SCORE_SLIDER)


def listen() -> None:
	FACE_ANALYSER_ORDER_DROPDOWN.change(update_face_analyser_order, inputs = FACE_ANALYSER_ORDER_DROPDOWN)
	FACE_ANALYSER_AGE_DROPDOWN.change(update_face_analyser_age, inputs = FACE_ANALYSER_AGE_DROPDOWN)
	FACE_ANALYSER_GENDER_DROPDOWN.change(update_face_analyser_gender, inputs = FACE_ANALYSER_GENDER_DROPDOWN)
	FACE_DETECTOR_MODEL_DROPDOWN.change(update_face_detector_model, inputs = FACE_DETECTOR_MODEL_DROPDOWN, outputs = [ FACE_DETECTOR_MODEL_DROPDOWN, FACE_DETECTOR_SIZE_DROPDOWN ])
	FACE_DETECTOR_SIZE_DROPDOWN.change(update_face_detector_size, inputs = FACE_DETECTOR_SIZE_DROPDOWN)
	FACE_DETECTOR_SCORE_SLIDER.release(update_face_detector_score, inputs = FACE_DETECTOR_SCORE_SLIDER)
	FACE_LANDMARKER_SCORE_SLIDER.release(update_face_landmarker_score, inputs = FACE_LANDMARKER_SCORE_SLIDER)


def update_face_analyser_order(face_analyser_order : FaceAnalyserOrder) -> None:
	bobacon.globals.face_analyser_order = face_analyser_order if face_analyser_order != 'none' else None


def update_face_analyser_age(face_analyser_age : FaceAnalyserAge) -> None:
	bobacon.globals.face_analyser_age = face_analyser_age if face_analyser_age != 'none' else None


def update_face_analyser_gender(face_analyser_gender : FaceAnalyserGender) -> None:
	bobacon.globals.face_analyser_gender = face_analyser_gender if face_analyser_gender != 'none' else None


def update_face_detector_model(face_detector_model : FaceDetectorModel) -> Tuple[gradio.Dropdown, gradio.Dropdown]:
	bobacon.globals.face_detector_model = face_detector_model
	update_face_detector_size('640x640')
	if face_analyser.pre_check():
		if bobacon.globals.face_detector_size in bobacon.choices.face_detector_set[face_detector_model]:
			return gradio.Dropdown(value = bobacon.globals.face_detector_model), gradio.Dropdown(value = bobacon.globals.face_detector_size, choices = bobacon.choices.face_detector_set[face_detector_model])
		return gradio.Dropdown(value = bobacon.globals.face_detector_model), gradio.Dropdown(value = bobacon.globals.face_detector_size, choices = [ bobacon.globals.face_detector_size ])
	return gradio.Dropdown(), gradio.Dropdown()


def update_face_detector_size(face_detector_size : str) -> None:
	bobacon.globals.face_detector_size = face_detector_size


def update_face_detector_score(face_detector_score : float) -> None:
	bobacon.globals.face_detector_score = face_detector_score


def update_face_landmarker_score(face_landmarker_score : float) -> None:
	bobacon.globals.face_landmarker_score = face_landmarker_score
