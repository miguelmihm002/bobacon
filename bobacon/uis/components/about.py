from typing import Optional
import gradio

from bobacon import metadata, wording

ABOUT_BUTTON : Optional[gradio.HTML] = None
DONATE_BUTTON : Optional[gradio.HTML] = None


def render() -> None:
	global ABOUT_BUTTON
	global DONATE_BUTTON

	ABOUT_BUTTON = gradio.Button(
		value = metadata.get('name') + ' ' + metadata.get('version'),
		variant = 'primary',
		link = metadata.get('url')
	)
	DONATE_BUTTON = gradio.Button(
		value = wording.get('uis.donate_button'),
		link = 'https://donate.bobacon.io',
		size = 'sm'
	)
