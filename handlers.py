"""Все что связано с аиограмом"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
"""Мои разбитые части кода(клавиатуры , состояния)"""
from keyboards import evalButton
from state import ElementsOfDiskriminant
from midlewares import TestMiddleware
"""Для работы с дискриминантом и графиком"""
import math
import matplotlib.pyplot as plt
import numpy as np
import os

router = Router()

router.message.outer_middleware(TestMiddleware)

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.set_state(ElementsOfDiskriminant.element_a)
    await message.answer(text = 'Good day! Please, enter the first element here', reply_markup = evalButton)

@router.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer(text = 'If you have a problem or have an idea to improve the quality of the bot, please contact @heroinecoсtail')

@router.message(ElementsOfDiskriminant.element_a)
async def first_element(message: Message, state: FSMContext):
    await state.update_data(a =  float(message.text))
    await state.set_state(ElementsOfDiskriminant.element_b)
    await message.reply(text = 'Good, please, enter the second element here')

@router.message(ElementsOfDiskriminant.element_b)
async def second_element(message: Message, state: FSMContext):
    await state.update_data(b = float(message.text))
    await state.set_state(ElementsOfDiskriminant.element_c)
    await message.reply(text = 'Good, please, enter the third element here')

@router.message(ElementsOfDiskriminant.element_c)
async def third_element(message: Message, state: FSMContext):
    await state.update_data(c = float(message.text))
    await state.set_state(ElementsOfDiskriminant.eval_result)
    await message.reply(text = 'Good! Now click on the button below...')

@router.message(ElementsOfDiskriminant.eval_result , F.text == "Press To Result🎌")
async def result_evals(message: Message, state: FSMContext):
    data = await state.get_data()
    result_1 = data["b"] ** 2 - 4 * data["a"] * data["c"]
    sqrt_D = math.sqrt(result_1)
    result_2 = (-data["b"] - sqrt_D) / (2 * data["a"])
    result_3 = (-data["b"] + sqrt_D) / (2 * data["a"])

    x = np.linspace(result_2 - 5, result_3 + 5, 400)
    y = data["a"] * x ** 2 + data["b"] * x + data["c"]

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()

    graph_image_path = 'FILE_ROAD'
    plt.savefig(graph_image_path)

    graph_image = FSInputFile(graph_image_path)
    await message.reply_photo(graph_image, caption= f'Result of multiplication:  \n D = {result_1} \n Root Discriminant: {sqrt_D}  \n x1 = {result_2} \n x2 = {result_3}')

    os.remove(graph_image_path)