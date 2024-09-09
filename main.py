import cv2
import numpy as np
from easyocr import Reader
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont

# распознавание и перевод текста
translator = Translator()
image_file = 'test3.jpg'
image = Image.open(image_file)
reader = Reader(['en'])

# распознание
results = reader.readtext(image_file, text_threshold=0.8)

# Создаем объект для рисования
draw = ImageDraw.Draw(image)

# Указываем новый текст и шрифт
font_path = '/usr/share/fonts/Roboto/Roboto-Light.ttf'
font_size = 15
font = ImageFont.truetype(font_path, font_size)

# Заменяем текст
for (bbox, text, prob) in results:
    if prob > 0.5:  # Убедимся, что уверены в распознавании текста

        translate_text = translator.translate(text, src='en', dest='ru').text

        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        # Проверка координат
        if bottom_right[1] >= top_left[1]:
            # Закрашиваем старый текст
            draw.rectangle([top_left, bottom_right], fill="white")

            # Добавляем новый текст
            draw.text((top_left[0], top_left[1]),
                      translate_text, fill="black", font=font)
        else:
            print(f"Неверные координаты: {top_left}, {bottom_right}")


# Сохраняем измененное изображение
output_path = 'output_image.png'
image.save(output_path)

print(f"Изображение сохранено как {output_path}")

# image = cv2.imread(image_file)

# strk = []

# result = Reader(['en']).readtext(image_file, detail=0,
#                                  paragraph=True, text_threshold=0.8)
# for i in result:
#     trans = translator.translate(i, src='en', dest='ru').text
#     strk.append(trans)
# print(strk)

# рамки вокруг распознанного текста

# result = Reader(['en']).readtext(image_file, text_threshold=0.8)
# print(result)

# for (coord, text, prob) in result:
#     # Рисуем ограничивающий прямоугольник
#     (topleft, topright, bottomright, bottomleft) = coord
#     tx, ty = (int(topleft[0]), int(topleft[1]))
#     bx, by = (int(bottomright[0]), int(bottomright[1]))
#     cv2.rectangle(image, (tx, ty), (bx, by), (255, 0, 0), 2)

# # Сохраняем обработанное изображение
# cv2.imwrite('result.jpg', image)

# print(text)
