# -*- coding: utf-8 -*-
from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    choosing_language = State()
    entering_fullname = State()
    entering_phone = State()


class MainMenu(StatesGroup):
    menu = State()


class SellHouse(StatesGroup):
    photos = State()
    ask_more_photo = State()
    region = State()
    district = State()
    price = State()
    extra_info = State()
    phone = State()


class BuyHouse(StatesGroup):
    region = State()
    district = State()
    browsing = State()


class RentOutHouse(StatesGroup):
    photos = State()
    price = State()
    region = State()
    district = State()
    location = State()
    extra_info = State()
    phone = State()


class RentInHouse(StatesGroup):
    region = State()
    district = State()
    browsing = State()
    waiting_location = State()


class MyAds(StatesGroup):
    listing = State()
