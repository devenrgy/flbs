name: 💡 Пожелание (Feature Request)
description: Предложите новую функцию или улучшение
title: "[FEATURE]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        ### 💡 Ваша идея
        Расскажите, что бы вы хотели добавить или улучшить в программе.

  - type: textarea
    id: problem
    attributes:
      label: Связано ли это с проблемой?
      description: Какую проблему решает ваше предложение?
      placeholder: Я хочу, чтобы программа могла...
    validations:
      required: false

  - type: textarea
    id: solution
    attributes:
      label: Описание решения
      description: Как именно это должно работать?
      placeholder: |
        Предлагаю добавить возможность...
        Это должно работать так...
    validations:
      required: true

  - type: textarea
    id: examples
    attributes:
      label: Примеры использования
      description: Как это будет выглядеть на практике?
      placeholder: |
        Пример команды: flbs.py --new-feature ...
        Ожидаемый результат: ...
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: Приоритет
      options:
        - 🔵 Низкий (просто идея)
        - 🟡 Средний (хотелось бы в будущем)
        - 🟠 Высокий (очень нужно)
        - 🔴 Критический (без этого невозможно работать)
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Альтернативы
      description: Какие есть обходные пути?
    validations:
      required: false

  - type: checkboxes
    id: contribute
    attributes:
      label: Готовы помочь?
      options:
        - label: Я готов помочь в реализации (PR welcome)
          required: false
