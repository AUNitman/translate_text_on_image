# import cv2
# import numpy as np
# from easyocr import Reader
# from googletrans import Translator
# from PIL import Image, ImageDraw, ImageFont

# # распознавание и перевод текста
# translator = Translator()
# image_file = 'test3.jpg'
# image = Image.open(image_file)
# reader = Reader(['en'])

# # распознание
# results = reader.readtext(image_file, text_threshold=0.8)

# # Создаем объект для рисования
# draw = ImageDraw.Draw(image)

# # Указываем новый текст и шрифт
# font_path = '/usr/share/fonts/Roboto/Roboto-Light.ttf'
# font_size = 15
# font = ImageFont.truetype(font_path, font_size)


# def get_background_color(image, bbox):
#     # Преобразуем изображение в массив NumPy для обработки
#     img_np = np.array(image)

#     # Получаем координаты
#     (top_left, top_right, bottom_right, bottom_left) = bbox
#     top_left = tuple(map(int, top_left))
#     bottom_right = tuple(map(int, bottom_right))

#     # Извлекаем область фона
#     background_area = img_np[top_left[1]                             :bottom_right[1], top_left[0]:bottom_right[0]]

#     # Возвращаем средний цвет области
#     return tuple(np.mean(background_area, axis=(0, 1)).astype(int))


# # Заменяем текст
# for (bbox, text, prob) in results:
#     if prob > 0.5:  # Убедимся, что уверены в распознавании текста

#         translate_text = translator.translate(text, src='en', dest='ru').text

#         (top_left, top_right, bottom_right, bottom_left) = bbox
#         top_left = tuple(map(int, top_left))
#         bottom_right = tuple(map(int, bottom_right))
#         back_color = get_background_color(image, bbox)

#         # Проверка координат
#         if bottom_right[1] >= top_left[1]:
#             # Закрашиваем старый текст
#             draw.rectangle([top_left, bottom_right], fill=back_color)

#             # Добавляем новый текст
#             draw.text((top_left[0], top_left[1]),
#                       translate_text, fill="black", font=font)
#         else:
#             print(f"Неверные координаты: {top_left}, {bottom_right}")


# # Сохраняем измененное изображение
# output_path = 'output_image.png'
# image.save(output_path)

# print(f"Изображение сохранено как {output_path}")


# test implaning
import cv2
import numpy as np
from easyocr import Reader
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont

# Загружаем изображение
image_file = 'test3.jpg'
image = cv2.imread(image_file)

translator = Translator()

# Инициализируем распознаватель текста
reader = Reader(['en'])

# Распознаем текст на изображении
results = reader.readtext(image_file)

# Создаем маску для инпейнтинга
mask = np.zeros(image.shape[:2], dtype=np.uint8)

# Заполняем маску областями текста и собираем координаты для вставки нового текста
text_boxes = []
for (bbox, text, prob) in results:
    if prob > 0.5:  # Уверенность распознавания
        points = np.array(bbox, dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)

        text_boxes.append(
            (bbox, translator.translate(text, src='en', dest='ru').text))

# Применяем инпейтинг для удаления текста
result = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# Преобразуем результат в PIL формат для работы со шрифтами
result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(result_pil)

# Устанавливаем путь к шрифту и размер шрифта
# Укажите путь к вашему шрифту
font_path = '/usr/share/fonts/Roboto/Roboto-Light.ttf'
font_size = 13  # Укажите нужный размер шрифта
font = ImageFont.truetype(font_path, font_size)

# Вставляем новый текст на место удаленного
for (bbox, text) in text_boxes:
    # Вычисляем координаты для вставки текста
    top_left = tuple(np.min(bbox, axis=0).astype(int))

    # Вставляем текст на изображение
    draw.text(top_left, text, font=font, fill=(0, 0, 0))

# Преобразуем обратно в формат OpenCV
result_cv2 = cv2.cvtColor(np.array(result_pil), cv2.COLOR_RGB2BGR)

# Сохраняем результат
output_path = 'output_image_with_text.png'
cv2.imwrite(output_path, result_cv2)

print(f"Изображение сохранено как {output_path}")
