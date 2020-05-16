import os
import pickle

from dotenv import load_dotenv
from rich.console import Console

from ui.displays import DebugDisplay
from ui.widgets import (
    ContainerWidget,
    CurrentPollenCountTextWidget,
    CurrentTemperatureTextWidget,
    CurrentWeatherIconWidget,
    HorizontalStackWidget,
    ImageWidget,
    SunsetTimeWidget,
    TabbedWidget,
    TextWidget,
    VerticalStackWidget,
)
from ui.windows import PilWindow

load_dotenv()

UI_IMAGE_PATH = os.getenv("UI_IMAGE_PATH")
UI_STATE_PATH = os.getenv("UI_STATE_PATH")

BBC_WEATHER_SAVE_PATH = os.getenv("BBC_WEATHER_SAVE_PATH")
OPEN_WEATHER_SAVE_PATH = os.getenv("OPEN_WEATHER_SAVE_PATH")

console = Console()


display = DebugDisplay(image_path=UI_IMAGE_PATH)
display.init()

widget = TabbedWidget(
    children=[
        ContainerWidget(
            size=(264, 176),
            child=HorizontalStackWidget(
                padding=25,
                children=[
                    CurrentPollenCountTextWidget(
                        weather_path=BBC_WEATHER_SAVE_PATH,
                        font_path="./assets/fonts/Roboto-Medium.ttf",
                        font_size=96,
                    ),
                    ImageWidget(size=(64, 64), path="./assets/icons/pollen.png"),
                ],
            ),
        ),
        ContainerWidget(
            size=(264, 176),
            child=HorizontalStackWidget(
                padding=25,
                children=[
                    CurrentTemperatureTextWidget(
                        weather_path=OPEN_WEATHER_SAVE_PATH,
                        font_path="./assets/fonts/Roboto-Medium.ttf",
                        font_size=96,
                    ),
                    CurrentWeatherIconWidget(
                        weather_path=OPEN_WEATHER_SAVE_PATH, size=(64, 64)
                    ),
                ],
            ),
        ),
        ContainerWidget(
            size=(264, 176),
            child=VerticalStackWidget(
                padding=5,
                children=[
                    TextWidget(
                        body="Sunset",
                        font_path="./assets/fonts/Roboto-Regular.ttf",
                        font_size=24,
                    ),
                    SunsetTimeWidget(
                        weather_path=os.getenv("OPEN_WEATHER_SAVE_PATH"),
                        font_path="./assets/fonts/Roboto-Medium.ttf",
                        font_size=72,
                    ),
                ],
            ),
        ),
        ContainerWidget(
            size=(264, 176),
            child=HorizontalStackWidget(
                padding=25,
                children=[
                    CurrentTemperatureTextWidget(
                        weather_path=OPEN_WEATHER_SAVE_PATH,
                        font_path="./assets/fonts/Roboto-Medium.ttf",
                        font_size=96,
                    ),
                    CurrentWeatherIconWidget(
                        weather_path=OPEN_WEATHER_SAVE_PATH, size=(64, 64)
                    ),
                ],
            ),
        ),
    ]
)

if os.path.exists(UI_STATE_PATH):
    with open(UI_STATE_PATH, "rb") as f:
        widget.set_state(pickle.load(f))

window = PilWindow(image_path=UI_IMAGE_PATH, width=264, height=176)

window.clear()

widget.draw(window)
window.save()
display.draw()

console.log("Updated display")

with open(UI_STATE_PATH, "wb") as f:
    pickle.dump(widget.state(), f)
