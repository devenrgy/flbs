name: 🐛 Сообщение об ошибке (Bug Report)
description: Сообщите об ошибке, чтобы мы могли её исправить
title: "[BUG]: <краткое описание ошибки>"
labels: ["bug"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Спасибо, что нашли время заполнить этот отчёт об ошибке!
        
  - type: textarea
    id: description
    attributes:
      label: Описание ошибки
      description: Подробно опишите, что произошло
      placeholder: Ошибка возникает когда...
    validations:
      required: true
      
  - type: textarea
    id: expected
    attributes:
      label: Ожидаемое поведение
      description: Что должно было произойти?
      placeholder: Я ожидал, что...
    validations:
      required: true
      
  - type: textarea
    id: reproduce
    attributes:
      label: Шаги воспроизведения
      description: Шаги для воспроизведения ошибки
      placeholder: |
        1. Запустить команду '...'
        2. Ввести '...'
        3. Увидеть ошибку
    validations:
      required: true
      
  - type: input
    id: version
    attributes:
      label: Версия программы
      description: Какую версию вы используете? (можно найти в релизах)
      placeholder: v1.0.0
    validations:
      required: true
      
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
      required: true
      
  - type: input
    id: python
    attributes:
      label: Версия Python
      description: Введите версию Python
      placeholder: python --version
    validations:
      required: true
      
  - type: textarea
    id: logs
    attributes:
      label: Логи/Вывод программы
      description: Скопируйте полный вывод программы или текст ошибки
      render: shell
    validations:
      required: false
      
  - type: textarea
    id: env
    attributes:
      label: Переменные окружения
      description: Укажите ваши переменные окружения (скройте чувствительные данные!)
      render: shell
      placeholder: |
        FLBS_PATH=/path/to/flibusta
        FLBS_INPX=flibusta.inpx
        FLBS_SAVE=/path/to/books
        FLBS_DB=/path/to/db
    validations:
      required: false
      
  - type: checkboxes
    id: terms
    attributes:
      label: Чек-лист
      description: Подтвердите, что вы проверили
      options:
        - label: Я проверил существующие issue и не нашёл похожей проблемы
          required: true
        - label: Я использую последнюю версию программы
          required: false
        - label: Все переменные окружения настроены корректно
          required: false
