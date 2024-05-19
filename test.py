import cv2
import sys
import numpy as np
import os

def збільшити_яскравість(image):
    if image.ndim == 2:  # перевірка, що зображення не одноканальне
        return image
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * 1.5, 0, 255)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

def зменшити_яскравість(image):
    if image.ndim == 2:  # перевірка, що зображення не одноканальне
        return image
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * 0.5, 0, 255)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

def обробити_зображення(image_path, вибрані_фільтри, save_path=None):
    image = cv2.imread(image_path)
    if image is None:
        print("Не вдалося завантажити зображення.")
        return

    for вибраний_фільтр in вибрані_фільтри:
        if вибраний_фільтр == 'розмиття':
            image = cv2.blur(image, (10, 10))
        elif вибраний_фільтр == 'підвищення насиченості':
            if image.ndim == 2:  # для одноканального зображення
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * 1.5, 0, 255)
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        elif вибраний_фільтр == 'Контурне виділення':
            image = cv2.Canny(image, 100, 200)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # перетворення назад у BGR
        elif вибраний_фільтр == 'відтінки сірого':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif вибраний_фільтр == 'негатив':
            image = 255 - image
        elif вибраний_фільтр == 'збільшення яскравості' or вибраний_фільтр == 'зменшення яскравості':
            if image.ndim == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            image = збільшити_яскравість(image) if вибраний_фільтр == 'збільшення яскравості' else зменшити_яскравість(image)
        elif вибраний_фільтр in ['агат', 'темно-синій', 'рожевий']:
            if image.ndim == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            image = cv2.applyColorMap(image, {
                'агат': cv2.COLORMAP_HOT,
                'темно-синій': cv2.COLORMAP_WINTER,
                'рожевий': cv2.COLORMAP_PINK
            }[вибраний_фільтр])

    if save_path:
        if os.path.exists(save_path):
            os.remove(save_path)
        cv2.imwrite(save_path, image)
        print(f"Оброблене зображення збережено за шляхом: {save_path}")
    else:
        cv2.imwrite(image_path, image)
        print(f"Оброблене зображення замінило оригінал: {image_path}")

def показати_доступні_фільтри():
    доступні_фільтри = ["розмиття", "підвищення насиченості", "Контурне виділення", "відтінки сірого", "негатив", "збільшення яскравості", "зменшення яскравості", "агат", "темно-синій", "рожевий"]
    print("Доступні фільтри:")
    for i, фільтр in enumerate(доступні_фільтри, start=1):
        print(f"{i}. {фільтр}")
    return доступні_фільтри

if __name__ == "__main__":
    while True:
        шлях_до_зображення = input("Введіть шлях до фото: ")
        if not шлях_до_зображення or not os.path.exists(шлях_до_зображення):
            print("Файл не знайдено, спробуйте ще раз.")
            continue
        else:
            break

    доступні_фільтри = показати_доступні_фільтри()
    вибрані_фільтри_ввід = input("Введіть номери фільтрів (через кому) або назви фільтрів, розділені комами:")
    вибрані_фільтри = [доступні_фільтри[int(i)-1] if i.isdigit() else i for i in вибрані_фільтри_ввід.split(",")]

    шлях_збереження = input("Введіть шлях для збереження обробленого зображення (або залиште порожнім для заміни оригіналу): ")
    обробити_зображення(шлях_до_зображення, вибрані_фільтри, шлях_збереження)
