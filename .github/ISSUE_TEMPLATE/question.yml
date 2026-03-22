name: ❓ Вопрос (Question)
description: Задайте вопрос по использованию программы
title: "[QUESTION]: "
labels: ["question"]
body:
  - type: markdown
    attributes:
      value: |
        ### ❓ Ваш вопрос
        Задайте вопрос как можно подробнее.

  - type: textarea
    id: question
    attributes:
      label: Вопрос
      description: Что вы хотите узнать?
      placeholder: Как использовать... / Можно ли... / Почему...
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Версия программы (если применимо)
      placeholder: v1.0.0
    validations:
      required: false

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
      required: false

  - type: textarea
    id: tried
    attributes:
      label: Что вы уже пробовали?
      description: Какие шаги вы предприняли для решения проблемы?
    validations:
      required: false

  - type: textarea
    id: context
    attributes:
      label: Дополнительная информация
      description: Всё, что может помочь ответить на ваш вопрос
    validations:
      required: false
