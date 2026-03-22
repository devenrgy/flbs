name: 💡 Запрос функции (Feature Request)
description: Предложите новую функцию или улучшение
title: "[FEATURE]: <краткое описание функции>"
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Спасибо за ваше предложение! Пожалуйста, заполните форму ниже.
        
  - type: textarea
    id: problem
    attributes:
      label: Связана ли ваша идея с проблемой?
      description: Опишите проблему, которую решит ваша функция
      placeholder: Я всегда сталкиваюсь с проблемой, когда...
    validations:
      required: false
      
  - type: textarea
    id: solution
    attributes:
      label: Описание решения
      description: Подробно опишите, как должна работать ваша функция
      placeholder: Я хотел бы, чтобы программа могла...
    validations:
      required: true
      
  - type: textarea
    id: alternatives
    attributes:
      label: Альтернативы
      description: Какие альтернативные решения вы рассмотрели?
      placeholder: Я пробовал...
    validations:
      required: false
      
  - type: textarea
    id: context
    attributes:
      label: Дополнительный контекст
      description: Добавьте скриншоты, примеры использования или другую информацию
    validations:
      required: false
      
  - type: dropdown
    id: priority
    attributes:
      label: Приоритет
      description: Насколько важна для вас эта функция?
      options:
        - Низкий (было бы неплохо)
        - Средний (хотелось бы увидеть в будущем)
        - Высокий (очень нужно)
        - Критический (без этого невозможно работать)
    validations:
      required: true
      
  - type: checkboxes
    id: terms
    attributes:
      label: Чек-лист
      options:
        - label: Я проверил существующие issue и не нашёл похожего предложения
          required: true
        - label: Я готов помочь в реализации этой функции (PR welcome)
          required: false
