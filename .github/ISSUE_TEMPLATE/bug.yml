name: 🐛 Баг (Ошибка)
description: Сообщите об ошибке в работе программы
title: "[BUG]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        ### 📋 Описание проблемы
        Опишите, что произошло и что вы ожидали увидеть.

  - type: textarea
    id: what-happened
    attributes:
      label: Что произошло?
      description: Подробно опишите ошибку
      placeholder: Например: Программа выдает ошибку при поиске книги...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Что должно было произойти?
      placeholder: Я ожидал, что...
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Шаги воспроизведения
      description: Как повторить ошибку?
      placeholder: |
        1. Запустил команду...
        2. Ввёл...
        3. Получил ошибку...
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Версия программы
      placeholder: v1.0.0
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Операционная система
      options:
        - Linux (Ubuntu/Debian)
        - Linux (Fedora/RHEL)
        - Linux (Arch/Manjaro)
        - Linux (Другой дистрибутив)
        - Windows
        - macOS
    validations:
      required: true

  - type: input
    id: python-version
    attributes:
      label: Версия Python
      placeholder: python --version
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Логи / Вывод программы
      description: Скопируйте текст ошибки
      render: shell
    validations:
      required: false

  - type: textarea
    id: env
    attributes:
      label: Переменные окружения
      description: Укажите ваши переменные (скройте пути, если нужно)
      render: shell
      placeholder: |
        FLBS_PATH=/path/to/flibusta
        FLBS_INPX=flibusta.inpx
        FLBS_SAVE=/path/to/books
        FLBS_DB=/path/to/db
    validations:
      required: false

  - type: textarea
    id: screenshots
    attributes:
      label: Скриншоты (если есть)
      description: Можно прикрепить скриншоты ошибки
    validations:
      required: false
