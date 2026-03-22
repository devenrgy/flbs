name: ❓ Вопрос (Question)
description: Задайте вопрос об использовании программы
title: "[QUESTION]: <краткое описание вопроса>"
labels: ["question"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Пожалуйста, задайте ваш вопрос как можно подробнее.
        
  - type: textarea
    id: question
    attributes:
      label: Ваш вопрос
      description: Подробно опишите, что вы хотите узнать
      placeholder: Как использовать... / Можно ли...
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
      description: На какой ОС вы работаете?
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
    id: context
    attributes:
      label: Дополнительный контекст
      description: Добавьте любую дополнительную информацию, которая может помочь
    validations:
      required: false
      
  - type: checkboxes
    id: terms
    attributes:
      label: Чек-лист
      options:
        - label: Я прочитал документацию (README.md)
          required: true
        - label: Я проверил существующие issue и не нашёл ответа на свой вопрос
          required: true
