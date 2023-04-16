from typing import List

from kivy.uix.widget import Widget
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRoundFlatIconButton
from kivymd.uix.chip import MDChip
from kivymd.uix.label import MDLabel

from samudra.interfaces import (
    KonsepData,
    KonsepToCakupanConnector,
    KonsepToKataAsingConnector,
)


def build_kata_asing_list(
    data: List[KonsepToKataAsingConnector], container: Widget, mode: str = None
) -> Widget:
    slot__kataasing = MDBoxLayout(orientation="horizontal", adaptive_height=True)
    if len(data) > 0:
        for kata_asing_connector in data:
            label = f"{kata_asing_connector.kata_asing.bahasa}: {kata_asing_connector.kata_asing.nama}"
            slot__kataasing.add_widget(MDChip(text=label, padding=(10, 0)))
    if mode == "edit":
        slot__kataasing.add_widget(
            MDChip(text="+", icon_right="translate", orientation="horizontal")
        )
    if len(slot__kataasing.children) > 0:
        container.add_widget(slot__kataasing)
    return container


def build_cakupan_list(
    data: List[KonsepToCakupanConnector], container: Widget, mode: str = None
) -> Widget:
    slot__cakupan = MDBoxLayout(orientation="horizontal", adaptive_size=True, spacing=5)
    if len(data) > 0:
        for cakupan_connector in data:
            slot__cakupan.add_widget(
                MDChip(text=cakupan_connector.cakupan.nama, padding=0)
            )
    if mode == "edit":
        slot__cakupan.add_widget(
            MDChip(text="+", icon_right="tag", orientation="horizontal")
        )
    if len(slot__cakupan.children) > 0:
        container.add_widget(slot__cakupan)
    return container


def build_konsep_list(
    data: List[KonsepData], container: Widget, mode: str = None
) -> Widget:
    box__konsep = MDBoxLayout(adaptive_height=True, spacing=5)
    if mode == "edit":
        box__konsep.add_widget(
            MDChip(text="+", icon_right="transcribe", orientation="horizontal")
        )
    for i, konsep in enumerate(data, 1):
        label = MDLabel(
            text="{}. [{:^6}] {}".format(i, konsep.golongan.id, konsep.keterangan)
        )
        if mode == "edit":
            btn__edit = MDIconButton(icon="pen", height=label.height)
            box__edit = MDBoxLayout(
                label,
                btn__edit,
                orientation="horizontal",
                padding=0,
                adaptive_height=True,
            )
            box__konsep.add_widget(box__edit)
        else:
            box__konsep.add_widget(label)
        build_kata_asing_list(konsep.kata_asing, container=box__konsep, mode=mode)
        build_cakupan_list(konsep.cakupan, container=box__konsep, mode=mode)
    container.add_widget(box__konsep)
    return container


def build_top_right_button(icon: str, on_release: callable) -> Widget:
    parent = MDAnchorLayout(anchor_x="right", anchor_y="top")
    btn__menu = MDIconButton(icon=icon)
    btn__menu.bind(on_release=on_release)
    parent.add_widget(btn__menu)
    return parent


def build_title(data: str, container: Widget, mode: str = None) -> Widget:
    container.add_widget(MDLabel(text=data, font_style="H2", underline=True, bold=True))
    return container
