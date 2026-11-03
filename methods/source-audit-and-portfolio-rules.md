# Итоговая экспертная приёмка — 31.10.2026

Это исторический отчёт проверки, не новый управляющий протокол и не дорожная карта. Он предшествует финальным уточнениям владельца 31.10.2026; прежние состояния WEB/PR, замечания о рассинхронизации и предложения о месте AI-консультанта не являются текущими заданиями. Полный текст снимков ниже сохранён для истории. Нормативные правила и последующие решения остаются в [AGENTS](../AGENTS.md), [плане v2](../references/project/ARCHITEKTONICA_SITE_PLAN_V2.md) и [протоколе](agent-expert-stage-protocol.md).

## A. Готовность экспертного агента

**READY WITH CONDITIONS.** Методики и экспертиза достаточны, чтобы начать этап 01. Безопасные противоречия ниже исправлены. Полная независимая оценка эффективности модели и будущая готовность production не подтверждены. Новый навык не требуется.

Базовая версия Creative: `ea24385` (main, merge PR #13); WEB: `002dfee` (main). Проверка выполнялась Codex (GPT-6) в текущем общем контексте; изолированный worktree `/workspace/expert-agent-acceptance`, Python 3.12.14, Node 24.19.0. Эти версии уточняются фактическим выводом команд в H. Новые чистые контексты и baseline не запускались. Никакие материалы этого отчёта не являются утверждённым контентом сайта.

Позиционирование сохранено буквально: **ARCHITEKTONICA — Архитектура решений.** / **Технологии · Дизайн · Бизнес**. Компания / company. Защищённый полный текст плана v2 и факты не изменены. Каталоги Creative/WEB совпали по всем полям и порядку: 17 направлений, 81 услуга.

Доступная репозиторная история подтверждает объединение PR #13. API GitHub отвечает `Forbidden`: состояние Actions, обсуждения PR/Issue и решения владельца вне репозитория недоступны. Во всём отчёте для результатов этапов 01–07 — `approval: unverified`; это не отрицание решений вне доступных источников.

## B. Проверка 21 навыка

Полные инструкции открыты для аудита. Пути — `skills/<имя>/SKILL.md`, зеркала — `.agents/skills/<имя>/SKILL.md`. Чтение explicit-only файла для аудита не является его активацией. Все YAML и зеркала проверены программно. Различия зеркал ограничены пересчётом относительных путей. Число 21 — снимок, не ограничение обнаружения.

| Навык | Когда применять | Ограничение | Собственные ресурсы | Проверяемый результат | Проверка / SHA256 SKILL (12 знаков) |
|---|---|---|---|---|---|
| `architektonica-creative-director` | Новая страница, согласование авторского решения | Не превращать техническую ссылку в кейс | — | Готовая концепция/страница | PASS структуры/зеркала; SKILL прочитан; `02de1981eb36` |
| `architektonica-reader-insight` | Роль читателя и ситуация выбора | Гипотеза не равна интервью | — | Сценарий и критерии выбора | PASS структуры/зеркала; SKILL прочитан; `5071d22a6013` |
| `architektonica-idea-lab` | Новый авторский ракурс | Не переизобретать утверждённую мысль | — | Предметная идея с опорой | PASS структуры/зеркала; SKILL прочитан; `e4e9e69af255` |
| `architektonica-narrative-design` | Драматургия страницы/кейса | Историческая карта не заменяет sitemap v2 | — | Последовательность и переходы | PASS структуры/зеркала; SKILL прочитан; `f4e0a405fea4` |
| `architektonica-copy-studio` | Тексты, услуги, UI-сообщения | Не изобретать факты и внедрение | — | Полный текст нужного жанра | PASS структуры/зеркала; SKILL прочитан; `83eeccdafed1` |
| `architektonica-psycholinguistic-editor` | Восприятие по F/M/ST-реестру | Не обещать доказанную нейроконверсию | — | Обоснованная правка | PASS структуры/зеркала; SKILL прочитан; `da84d50df2cd` |
| `architektonica-critical-editor` | Редактура готового материала | Сохранять сильный голос; не квоты | — | Исправленный текст | PASS структуры/зеркала; SKILL прочитан; `23bcec2dcb53` |
| `architektonica-search-visibility` | IA, SEO/GEO/AEO, метаданные | Не выдумывать частотность/цитирование | — | Карта намерений либо метаданные | PASS структуры/зеркала; SKILL прочитан; `ae9a1a193d5f` |
| `architektonica-engine-mapper` | Явное заполнение Excel | Копия исходника; сохранить ID/колонки | — | Проверенный XLSX при поручении | PASS структуры/зеркала; SKILL прочитан; `5fba62f9139f` |
| `architektonica-portfolio-case-writer` | Оформление работы в портфолио | URL вне этого контекста не триггер | — | Кейс/карточка/SEO/медиаплан | PASS структуры/зеркала; SKILL прочитан; `be3c51e4e6b7` |
| `architektonica-ui-ux-expert` | IA, композиция, адаптация Engine | Выдача Pro Max — гипотеза; PHP сохраняется | content-model.md | Модель/контракт блока | PASS структуры/зеркала; SKILL прочитан; `0f0e3050dc06` |
| `architektonica-website-qa` | Проверка реализованного preview | Нет браузера — нет визуального PASS | QA_CHECKLIST.md | Дефекты и evidence matrix | PASS структуры/зеркала; SKILL прочитан; `a74b7af4eff7` |
| `emil-design-eng` | Интерфейсные детали и визуальная точность | React-примеры не разрешают смену стека | — | Обоснованное UI-решение | PASS структуры/зеркала; SKILL прочитан; `ffbe68e6007f` |
| `animate` | Реализация оправданного движения | RECIPES; не устанавливать библиотеку ради fade | RECIPES.md | Код и reduced-motion | PASS структуры/зеркала; SKILL прочитан; `b8ede1612704` |
| `animation-performance` | Диагностика медленных сцен | Read-only; GPU/FPS только по trace | — | Причина и измеряемая рекомендация | PASS структуры/зеркала; SKILL прочитан; `ceb9dd3fe912` |
| `find-animation-opportunities` | Поиск уместных движений | Read-only; не автоматическая реализация | — | Отобранные/отклонённые возможности | PASS структуры/зеркала; SKILL прочитан; `d52a377819b8` |
| `improve-animations` | Аудит motion и планы | Read-only; execute не обходит explicit-only | AUDIT.md, PLAN-TEMPLATE.md | Аудит и план при поручении | PASS структуры/зеркала; SKILL прочитан; `739624474644` |
| `review-animations` | Явный вызов для motion-review | explicit-only; STANDARDS; без реализации | STANDARDS.md | Ревью, не owner approval этапа | PASS структуры/зеркала; SKILL прочитан; `6ff590d29e43` |
| `prototype` | Явный вызов для вариантов UI | explicit-only; PICKER; изоляция от production | PICKER.md | Рабочие варианты и выбор владельца | PASS структуры/зеркала; SKILL прочитан; `bba39c955eb1` |
| `mobile-native` | Touch, viewport, мобильное поведение | Не объявлять real-device проверку по эмулятору | — | Исправление и проверка на устройстве | PASS структуры/зеркала; SKILL прочитан; `888b7651d66d` |
| `break-ui` | Пограничные данные/состояния UI | CATALOG; фикстуры только dev; scope поручения | CATALOG.md | Воспроизводимый дефект и проверка | PASS структуры/зеркала; SKILL прочитан; `e7eec1d70ac5` |

Зависимые проектные источники перечислены в самих SKILL и динамическом каталоге; их локальные пути проверяет verifier. Девять Emil и их рецепты, лицензия `third_party/emil-skills-LICENSE`, выборочная MIT-поставка `third_party/ui-ux-pro-max` сохранены. Внешние маршруты `pick-ui-library`/`animate-expo` не установлены и не считаются работающими. Правила производственной адаптации имеют приоритет над примерами сторонних стеков. Работоспособность каждого из 21 навыка в собственном независимом LLM-сеансе **NOT RUN**; пять доступных контрольных решений — ниже.

## C. Реальное применение: пять контрольных решений

Источник заданий: [fixtures](../tests/fixtures/skill-evaluation-cases.json); процедура: [оценка навыков](skill-effectiveness-evaluation.md). Это выполненные текстовые решения в текущем контексте и их авторская самопроверка. **Чистые контексты, baseline без навыков и независимые человеческие оценки 0/1/2: NOT RUN.** Баллы не выставлены автором самому себе. Полная приёмка поведения — NOT VERIFIED; конкретные проверки ограничений ниже — PASS, где есть прямое доказательство в результате.

### C1. home — главная

Этап 01: предложенная структура; тексты этапа 02 — разрешённая заданием предварительная подготовка. `approval: unverified`. Прочитаны creative-director, reader-insight, idea-lab, narrative-design, copy-studio, critical-editor; источники — Brand Core, Fact Bank, Case Studies, голос и каталог. Применены: три роли читателя из reader-insight; схема «разные миры → общая логика → самостоятельные практики» из narrative-design; фактическая граница copy-studio.

**Первый экран:**

> ARCHITEKTONICA — Архитектура решений.
>
> Технологии · Дизайн · Бизнес
>
> У задачи есть поверхность — то, что видит человек. И устройство — то, от чего зависит его следующий шаг. Мы работаем с обоими: проектируем цифровые продукты, AI-системы и коммуникацию бизнеса.
>
> Посмотреть проекты

**Проекты / «Масштаб меняет декорации. Точность остаётся».**

> Рабочая среда химика и сайт будущего дома требуют разных решений. В Synapto мы разработали архитектуры AI-платформы и отдельный интерфейсный прототип. На сайте «Сторис на Мосфильмовской» пять историй помогают представить дом — от расположения до планировки.

Карточки показывают точную стадию и известную роль; наличие публичных страниц ещё проверяется. Кнопку не превращать в несуществующий URL.

**Практики / «У каждой задачи — свой инструментарий».**

> Брендинг, цифровые продукты, AI, визуальные проекты и бизнес-практики раскрываем по собственным рабочим ситуациям. В каталоге — 17 направлений и 81 услуга: от айдентики до архитектуры AI-решения и бизнес-аналитики.

Полный каталог доступен независимо от числа входных навигационных групп.

**Подход / «Прежде чем двигать пиксели, определяем, что должно измениться».**

> Уточняем задачу, проектируем устройство решения и содержание. Затем выбираем форму, собираем интерфейс и проверяем его в работе. Так у каждого выразительного решения появляется основание.

**Статьи.** Показывать контекстные превью только реальных опубликованных материалов; пока их нет, блок не заполняется вымышленными публикациями.

**Завершение / «С какой задачи начнём?»**

> Расскажите, что вы создаёте и какое решение сейчас требует внимания.
>
> Перейти к контактам

Самопроверка: точный дескриптор/три опоры/компания — PASS; стадии Synapto разделены — PASS; нет KPI/выдуманных клиентов — PASS; структура не привязана к слотам Engine — PASS. Это кандидат текста, не запись в Copy Registry. Согласование, пользовательский тест понимания, проверка реального CTA и визуальная посадка — NOT RUN.

### C2. service — «Архитектура AI-решения»

Этап 01: содержание и связи; черновой текст этапа 02. Прочитаны ui-ux-expert, copy-studio, search-visibility, reader-insight; ресурс `skills/architektonica-ui-ux-expert/references/content-model.md`. Источник: точная услуга из направления «AI-системы: проектирование и разработка» в [каталоге](../references/project/services_catalogue.json). В реестре ещё нет стабильных service ID: `svc-ai-solution-architecture` — **предлагаемый ID**, не утверждённый существующий идентификатор; slug также не утверждён.

**H1: Архитектура AI-решения**

> Уверенный ответ модели ещё не означает, что система готова к работе. Нужно определить, откуда приходят данные, кому доступен результат и что происходит, когда модель ошибается.
>
> Проектируем компоненты AI-системы, выбор моделей, потоки данных, API и интеграции. Фиксируем требования к инфраструктуре, безопасности и доступам, план тестирования, наблюдаемости и масштабирования.

**Когда обращаться.** Когда применение AI уже рассматривается, но необходимо определить границы системы, условия её проверки и место в действующих процессах. Это рабочая гипотеза аудитории руководителя/технического ответственного, не цитата интервью.

**Что получает проект.** Схему компонентов и связей; решения по моделям и данным; контур интеграций и доступов; требования к инфраструктуре; план проверки. Уточнённый состав и границы артефактов фиксируются под задачу.

**Предметное подтверждение.** В Synapto разработаны архитектуры AI-платформы для двух фармацевтических компаний. Отдельно построен интерфейсный прототип рабочей среды. Они показывают различие между устройством будущей системы и её интерфейсом; внедрение и экономический эффект этим не подтверждаются.

**Следующий шаг.** Обсудить задачу и доступные данные — без обещания срока ответа или автоматического запуска разработки.

Связи: предложить W1-A1/W1-A2 и W2 после проверки публичности конкретной страницы; W1-P отмечать как отдельный прототип. Статьи пока только редакционные темы («Как проверять AI до внедрения»), без вымышленных URL, автора и даты. Title-кандидат: «Архитектура AI-решения | ARCHITEKTONICA». EN — непереведённый черновик; hreflang до появления опубликованной взаимной версии не добавлять.

Самопроверка: точное название/scope услуги — PASS; ID честно предложен — PASS; нет пустых ссылок — PASS; содержание отделено от последующего визуального проектирования — PASS. Утверждение ID/URL/страницы, полнота реального перевода и публикация — NOT RUN.

### C3. case-uncertain — архитектура и прототип

Этап 02, предварительное упражнение; approval предыдущего этапа не подтверждён. Прочитаны portfolio-case-writer и critical-editor, Fact Bank §1/§6, методика portfolio-case-workflow. Исходные факты фиксированы: созданы архитектура и прототип; внедрение/эффект не подтверждены. Название, клиент и функции не предоставлены. Не подставляем Synapto автоматически вместо неизвестного проекта.

**Предварительный кейс / H1: «Архитектура и прототип: две части проектного решения»**

> В этой работе созданы архитектура системы и прототип. Архитектура задаёт устройство решения; прототип позволяет рассмотреть его до следующего этапа разработки.

**Устройство.** Подготовленная архитектура — самостоятельный результат проектирования. Детали компонентов и интеграций добавляются после получения исходных материалов.

**Прототип.** Второй результат — прототип. Его наличие не подтверждает ни готовность всей системы, ни работу в реальных процессах заказчика.

**На чём заканчивается этот этап.** В кейсе можно показать созданные артефакты. Выводы о запуске, скорости работы и пользе для бизнеса потребуют отдельных подтверждений.

Карточка: «Архитектура системы и прототип. Проектная работа перед дальнейшей разработкой; результаты внедрения не заявлены». Meta title-кандидат: «Архитектура системы и прототип | ARCHITEKTONICA». Медиа-план: реальная схема архитектуры и реальные изображения прототипа при их предоставлении; они не объявлены уже доступными. Для полноценного публичного кейса недостаёт названия/публичности, роли автора и конкретного сценария. Упражнение выполнено, **публичный выпуск заблокирован недостатком фактуры**.

Самопроверка: нет фиктивного клиента, функций и цифр — PASS; стадии не смешаны — PASS; полный содержательный кейс по этим данным — PARTIAL. Человеческая оценка стиля и подтверждение публикации — NOT RUN. Это честное ограничение, а не повод сочинить детали.

### C4. microcopy — отключённая форма

Этап 02: проектирование состояний; реализация — этап 05. Прочитаны copy-studio, psycholinguistic-editor, critical-editor; исследовательская карта M09/F16 (малый ясный шаг, без заявленного эффекта на конверсию), `site-analytics-contract.md`; read-only сверка WEB `includes/contact.php`.

| Состояние | Текст-кандидат | Условие |
|---|---|---|
| Отключённый preview | «Форма пока недоступна. Сообщения не отправляются и не сохраняются» | Кнопка disabled, статус объяснён рядом; не выдавать отключённую форму за работающую |
| Кнопка будущей рабочей формы | «Отправить сообщение» | Активировать после реализации backend |
| Пустое обязательное поле | «Введите адрес электронной почты» | Только если поле действительно обязательное |
| Ошибка формата | «Проверьте адрес: например, name@example.com» | Соответствует принятому валидатору |
| Сервер не подтвердил приём | «Не удалось подтвердить приём сообщения. Попробуйте ещё раз» | Не утверждать, что обращение точно потеряно; повтор защищён idempotency |
| Подтверждённый приём | «Сообщение принято» | Только по подтверждённому backend; не обещать доставку конкретному сотруднику |

Самопроверка: ясные действия/«вы»/нет маркетинговой иронии в ошибке — PASS; несуществующий email компании и время ответа не придуманы — PASS; preview не создаёт успех или lead_confirmed — PASS на уровне предложенного контракта. Реальная серверная форма, доставка и события аналитики — NOT RUN.

### C5. immersive-scene — глубина, поддерживающая смысл

Этап 04: подготовительный проект сцены, без утверждения результатов 01–03. Прочитаны ui-ux-expert, emil-design-eng (пространственная непрерывность, 3D transform, hover gating), animation-performance (сначала причина/trace, не will-change), mobile-native (svh/dvh, safe areas, touch), производственная методика и QA checklist. Автоматически prototype/review-animations не активировались. Код в WEB не создавался.

**Решение:** блок «Архитектура AI-решения» раскрывает путь данных через модель к проверке специалистом. Это схема предлагаемой услуги, не схема неизвестной внедрённой системы.

- Передний план: читаемый H2 и краткий аргумент в обычном DOM. Средний: подписанная схема «Данные → Модель → Проверка специалистом». Дальний: крупная спокойная плоскость. Масштаб, перекрытие и светотень создают глубину без движения; перспектива задаётся CSS perspective, а не одним z-index.
- Основная реализация — HTML/CSS, существующие GSAP/ScrollTrigger; Lenis интегрируется через один согласованный ticker, без второго RAF. WebGL/Three.js **для этой схемы не нужен**; он остаётся отдельной возможностью при доказанном выигрыше. Это выбор инструмента, не пробел компетенции.
- Скролл немного меняет дистанцию между декоративными планами. Текст и CTA не зависят от раскрытия; обязательный pinned-scroll не нужен. Фокус/клавиатура и нативная прокрутка доступны. Указатель влияет только при hover:hover/pointer:fine; взаимодействие не требует hover.
- На телефоне — вертикальная статичная схема, полный текст, без тяжёлого параллакса. При reduced-motion/no-JS сохраняются схема, масштабная иерархия и все действия.
- GSAP context/timelines/ScrollTrigger уничтожаются при выходе; Lenis не создаётся на каждый блок. Offscreen/hidden работа приостанавливается; refresh после загрузки шрифтов/медиа. Если позже появится WebGL: ограничить DPR, обработать context loss, dispose геометрию/материалы/текстуры/render targets и предоставить статический DOM-эквивалент.
- Приёмка: desktop/tablet/mobile, повторный вход/назад/bfcache, быстрый scroll, смена ориентации, клавиатура/reduced-motion. Профилировать frame-time, long tasks, память/слушатели и медиа на целевом смартфоне; до/после повторных входов. Согласовать бюджеты после исходного замера. Lighthouse не равен полевым CWV; вымышленных FPS нет.

Самопроверка назначения/статичной глубины/стека/fallback/cleanup — PASS по спецификации. Работающий образец, браузерные снимки и реальные измерения — NOT RUN. Gate этапа 04 не пройден.

## D. Полная матрица этапов 01–07

Каждая из 51 маркированной работы неизменённого плана v2 представлена отдельной строкой. Далее добавлены уточнения из задания по особым страницам, scene lifecycle и QA. Матрица — отчёт покрытия, не новый план. Источник каждой строки — [план](../references/project/ARCHITEKTONICA_SITE_PLAN_V2.md), соответствующий основной SKILL и указанная дополнительная методика. Действие выполняет агент, технические действия — в WEB на разрешённом этапе; Gate принимает только владелец. `READY` относится к подготовленности методики; результат сайта обозначен отдельно. Для всех Gate сейчас `approval: unverified`.

| Этап | Задача плана | Ответственный навык/компетенция | Дополнительные навыки | Источник | Действие агента | Результат | Самопроверка | Gate владельца | Статус | Пробел |
|---|---|---|---|---|---|---|---|---|---|---|
| 01.01 | Определить полную карту сайта и навигацию. | architektonica-creative-director | reader-insight, narrative-design | [architektonica-creative-director](../skills/architektonica-creative-director/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: sitemap и входные сценарии | Sitemap и входные сценарии | Все обязательные разделы, нет сиротских страниц | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | Не утверждены sitemap/URL |
| 01.02 | Структурировать все 17 направлений и 81 услугу без сокращения каталога. | architektonica-ui-ux-expert | search-visibility | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: таблица 17/81 и группировки | Таблица 17/81 и группировки | Ровно 81 уникальная услуга, 17 направлений; названия/объёмы из реестра | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | Группировка пока предложение |
| 01.03 | Определить, каким услугам необходимы самостоятельные подробные страницы, а каким достаточно представления в общем каталоге и внутри направлений. | architektonica-reader-insight | search-visibility, ui-ux-expert | [architektonica-reader-insight](../skills/architektonica-reader-insight/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: решение detail_page для каждой услуги | Решение detail_page для каждой услуги | Обоснование полезности отдельной страницы; нет 81 автоматической пустой страницы | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | Нужны решения владельца |
| 01.04 | Спроектировать главную, страницы услуг, портфолио, кейсы, «О компании», «Как мы работаем», «Блог / Статьи», «Вакансии», контакты и вспомогательные разделы. | architektonica-creative-director | narrative-design, ui-ux-expert | [architektonica-creative-director](../skills/architektonica-creative-director/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: полный перечень типов страниц | Полный перечень типов страниц | Главная, направления/детали, кейсы, about, процесс, blog/статья, careers, контакты, legal/служебные | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | Реализована лишь часть шаблонных маршрутов WEB |
| 01.05 | Продумать взаимосвязи между услугами, кейсами и статьями. | architektonica-ui-ux-expert | search-visibility | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: карта связей service–case–article | Карта связей Service–Case–Article | Двусторонние ссылки, stage/publication status, нет черновых целей | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | Нет утверждённых публикаций |
| 01.06 | Определить структуру русской и английской версий. | architektonica-search-visibility | ui-ux-expert | [architektonica-search-visibility](../skills/architektonica-search-visibility/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: ru/en url-стратегия и translation | RU/EN URL-стратегия и Translation | Стабильные ID отдельно от slug; взаимные опубликованные hreflang | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | EN-переводы не подтверждены |
| 01.07 | Предусмотреть место клиентского кабинета и будущего AI-консультанта. | architektonica-creative-director | reader-insight | [architektonica-creative-director](../skills/architektonica-creative-director/SKILL.md); [методика](../skills/architektonica-ui-ux-expert/references/content-model.md) | Спроектировать и обосновать: место кабинета и будущего консультанта | Место кабинета и будущего консультанта | Без выдуманных функций и неработающего входа; отдельный цикл платформы | Полная карта/навигация; approval: unverified | READY методика; PLANNED результат | Endpoint не подтверждён |
| 02.01 | Подготовить полные тексты главной страницы. | architektonica-copy-studio | creative-director, critical-editor | [architektonica-copy-studio](../skills/architektonica-copy-studio/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: полная главная по принятой структуре | Полная главная по принятой структуре | Дескриптор, три опоры, реальные проекты; нет штампов/фейковых KPI | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Контрольный кандидат C1 не утверждён |
| 02.02 | Разработать содержательные описания всех 81 услуг. | architektonica-copy-studio | reader-insight, search-visibility | [architektonica-copy-studio](../skills/architektonica-copy-studio/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: 81 содержательное описание | 81 содержательное описание | Имена/scope сверены с реестром; не удалены близкие услуги | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Корпус 81 текста не создан в этом аудите |
| 02.03 | Написать тексты направлений, About, процесса и контактов. | architektonica-copy-studio | narrative-design, critical-editor | [architektonica-copy-studio](../skills/architektonica-copy-studio/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: тексты направлений/about/процесса/контактов | Тексты направлений/About/процесса/контактов | Один голос; реальные контакты; кабинет только по фактам | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Нужны утверждённые контакты |
| 02.04 | Подготовить публикационные кейсы на основе реальных проектов. | architektonica-portfolio-case-writer | critical-editor, search-visibility | [architektonica-portfolio-case-writer](../skills/architektonica-portfolio-case-writer/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: кейс, карточка, seo и медиаплан | Кейс, карточка, SEO и медиаплан | Роль/стадия/публичность; не превращать прототип в внедрение | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Недостающие факты не заполнять вымыслом |
| 02.05 | Спроектировать редакционную структуру блога и подготовить первые статьи. | architektonica-copy-studio | narrative-design, ui-ux-expert | [architektonica-copy-studio](../skills/architektonica-copy-studio/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: редакционная модель и первые статьи | Редакционная модель и первые статьи | Тема/содержание/связи; не выдумывать автора/дату | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Реальных первых статей пока не подтверждено |
| 02.06 | Создать заголовки, пояснения, микротексты, CTA и FAQ. | architektonica-copy-studio | psycholinguistic-editor, critical-editor | [architektonica-copy-studio](../skills/architektonica-copy-studio/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: h1/cta/faq и ui-состояния | H1/CTA/FAQ и UI-состояния | M09 без давления; нет ложного успеха формы; понятное действие | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | C4 — проект текстов, не работающая форма |
| 02.07 | Согласовать смысловые переходы между блоками. | architektonica-narrative-design | copy-studio, critical-editor | [architektonica-narrative-design](../skills/architektonica-narrative-design/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: последовательность переходов | Последовательность переходов | Блоки продвигают мысль; случайные повторы устранены | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Требуется корпус всех страниц |
| 02.08 | Подготовить SEO-структуру и внутренние связи. | architektonica-search-visibility | copy-studio | [architektonica-search-visibility](../skills/architektonica-search-visibility/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: title/description/h1 и внутренняя перелинковка | Title/description/H1 и внутренняя перелинковка | Проверяемые entity/schema; без фиктивной частотности | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Консоли и live-данные не доступны |
| 02.09 | Определить необходимые изображения, видео, иллюстрации и 3D-материалы. | architektonica-engine-mapper | ui-ux-expert, portfolio-case-writer | [architektonica-engine-mapper](../skills/architektonica-engine-mapper/SKILL.md); [методика](site-voice-and-consistency.md) | Спроектировать и обосновать: медиаплан с происхождением/правами | Медиаплан с происхождением/правами | Существующие медиа отделены от предложенных; ID Excel только при экспорте | Полный корпус содержания; approval: unverified | READY методика; PLANNED результат | Нужно собрать и подтвердить реальные активы |
| 03.01 | Какую задачу посетителя он решает. | architektonica-reader-insight | ui-ux-expert | [architektonica-reader-insight](../skills/architektonica-reader-insight/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: задача читателя в контракте блока | Задача читателя в контракте блока | Действие и аудитория определены, не отвлечённая декорация | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Контракт конкретного блока ещё не утверждён |
| 03.02 | Какой текст и какие факты раскрывает. | architektonica-copy-studio | critical-editor | [architektonica-copy-studio](../skills/architektonica-copy-studio/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: источник текста/фактов и approval_ref | Источник текста/фактов и approval_ref | Совпадение с утверждённой версией, без смысловой подмены | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Нужен принятый контент этапа 02 |
| 03.03 | Какая композиция помогает лучше понять содержание. | architektonica-ui-ux-expert | emil-design-eng | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: композиция/типографика/токены | Композиция/типографика/токены | Реальный длинный RU/EN текст, иерархия, контраст, состояния | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Утверждённые образцы отсутствуют |
| 03.04 | Какой визуальный материал необходим. | architektonica-ui-ux-expert | portfolio-case-writer | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: решение о визуальном материале | Решение о визуальном материале | Материал объясняет содержание; права и загрузка учтены | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Нужен медиаплан/активы |
| 03.05 | Как блок взаимодействует с соседними. | architektonica-narrative-design | emil-design-eng | [architektonica-narrative-design](../skills/architektonica-narrative-design/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: переходы и интерактивные состояния | Переходы и интерактивные состояния | Логика чтения/фокуса, соседние блоки и CTA согласованы | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Нужен рабочий образец |
| 03.06 | Что из Engine сохраняется, дорабатывается, расширяется или заменяется. | architektonica-ui-ux-expert | engine-mapper | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: retain/rework/extend/replace с причиной | retain/rework/extend/replace с причиной | Сохранены сильные решения Engine; не подгонять текст под слоты | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Не утверждено по конкретным блокам |
| 03.07 | Как блок ведёт себя на смартфоне. | mobile-native | ui-ux-expert, break-ui | [mobile-native](../skills/mobile-native/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: адаптивные состояния блока | Адаптивные состояния блока | 320 CSS px, touch/клавиатура, длинные строки, safe areas | Дизайн/блоки/прототипы; approval: unverified | READY методика; PLANNED результат | Нужны браузер и реальные устройства |
| 04.01 | Передний, средний и дальний композиционные планы. | architektonica-ui-ux-expert | emil-design-eng | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: статичная трёхплановая композиция | Статичная трёхплановая композиция | Текст/действия доступны без motion; ясная иерархия | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | C5 — спецификация без образца |
| 04.02 | Перспектива, масштаб, перекрытия, светотень, объём. | architektonica-ui-ux-expert | emil-design-eng | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: перспектива, масштаб и светотень | Перспектива, масштаб и светотень | z-index не выдан за перспективу; контраст/читаемость | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | Визуальная проверка NOT RUN |
| 04.03 | Продуманные скролл-переходы и параллакс. | animate | animation-performance, mobile-native | [animate](../skills/animate/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: scrolltrigger-сцена с fallback | ScrollTrigger-сцена с fallback | Один ticker/Lenis; нативная прокрутка; быстрый scroll/resize/bfcache | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | Нужны код и traces |
| 04.04 | Реакции интерфейса на курсор и действия посетителя. | animate | mobile-native, emil-design-eng | [animate](../skills/animate/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: реакции pointer/touch/keyboard | Реакции pointer/touch/keyboard | Hover gating, нет обязательного hover, мгновенные частые действия | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | Нужен рабочий образец |
| 04.05 | CSS 3D и выборочные Three.js/WebGL-сцены. | architektonica-ui-ux-expert | animation-performance | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: обоснованный css3d либо webgl | Обоснованный CSS3D либо WebGL | DPR/media budget, context loss, dispose и DOM fallback | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | Инструмент выбирается по смыслу, не автоматически |
| 04.06 | Кинематографичные переходы между смысловыми фрагментами. | animate | narrative-design, mobile-native | [animate](../skills/animate/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: переходы между смысловыми сценами | Переходы между смысловыми сценами | Контент не заперт до проигрывания; reduced-motion | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | Проверить согласованный прототип |
| 04.07 | Единая система ритма, длительностей и характера движения. | animate | animation-performance | [animate](../skills/animate/SKILL.md); [методика](engine-template-adaptation.md) | Спроектировать и обосновать: общие motion-токены/ритм | Общие motion-токены/ритм | Продолжительность по задаче; не новый параллельный набор токенов | Образцы desktop/mobile/motion; approval: unverified | READY методика; PLANNED результат | Числа после контекста/замеров |
| 05.01 | Сохранить существующий PHP-проект как техническую отправную точку. | PHP/Beget | ui-ux-expert | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: php bootstrap/router/layout сохранены | PHP bootstrap/router/layout сохранены | Lint/routes/404/301/405 и совместимость Engine | Функциональный preview; approval: unverified | READY методика; PLANNED результат | PHP CLI отсутствует в текущей среде |
| 05.02 | Перестроить необходимые шаблоны, страницы и компоненты Engine. | architektonica-ui-ux-expert | emil-design-eng | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: php-компоненты/шаблоны под контент | PHP-компоненты/шаблоны под контент | Approved source snapshot и diff, нет React-миграции | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Требуются gates 01–04 |
| 05.03 | Реализовать утверждённые блоки и взаимодействия. | emil-design-eng | animate, mobile-native | [emil-design-eng](../skills/emil-design-eng/SKILL.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: утверждённые интерактивные блоки | Утверждённые интерактивные блоки | Состояния, keyboard/reduced-motion, точечные тесты | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Требуются принятые образцы |
| 05.04 | Подключить полный каталог услуг и реальные кейсы. | PHP/Beget | website-qa, critical-editor | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: каталог и реальные кейсы на страницах | Каталог и реальные кейсы на страницах | Сравнение всех полей 17/81; публичность/стадии кейсов | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Каталог уже совпадает; демо-карточки остаются |
| 05.05 | Создать систему публикаций блога и страниц статей. | PHP/Beget | ui-ux-expert, search-visibility | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: публикационная система и статья | Публикационная система и статья | ID/status/locale, экранирование/доступ; удобство редактирования | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Есть шаблон коллекции, не утверждённая CMS |
| 05.06 | Реализовать адаптивность и облегчённые варианты сложных эффектов. | mobile-native | animate, animation-performance | [mobile-native](../skills/mobile-native/SKILL.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: адаптивность и облегчённые сцены | Адаптивность и облегчённые сцены | Мобильная композиция/клавиатура/WebGL/no-JS fallbacks | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Нужны real-device испытания |
| 05.07 | Настроить рабочие формы обращений. | PHP/Beget | website-qa, copy-studio | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: серверный приём обращений | Серверный приём обращений | CSRF/лимиты/idempotency/приём-доставка; ошибки не успех | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Preview намеренно отклоняет отправку |
| 05.08 | Подключить SEO-метаданные, аналитику и необходимые интеграции. | architektonica-search-visibility | website-qa, PHP/Beget | [architektonica-search-visibility](../skills/architektonica-search-visibility/SKILL.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: seo и события аналитики | SEO и события аналитики | Canonical/hreflang для реальных локалей; lead_confirmed; consent/PII | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Система аналитики и события не внедрены |
| 05.09 | Организовать разработку через отдельные ветки, preview и проверяемые Pull Requests. | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Реализовать в WEB: feature-ветка, reviewable pr и preview | Feature-ветка, reviewable PR и preview | Checks привязаны к commit; noindex; merge только владельцем | Функциональный preview; approval: unverified | READY методика; PLANNED результат | Git доступен; API/CI не подтверждены |
| 06.01 | Проверить точность контента и отсутствие демонстрационных данных Engine. | architektonica-critical-editor | website-qa, search-visibility | [architektonica-critical-editor](../skills/architektonica-critical-editor/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Проверить в WEB: сверка всего публикационного корпуса | Сверка всего публикационного корпуса | Факты/стадии/имена/контакты; нет демо/фейковых KPI | Сайт без P0/P1; approval: unverified | READY методика; NOT VERIFIED исполнение | В WEB остаётся Engine-контент |
| 06.02 | Протестировать все маршруты, формы и навигацию. | architektonica-website-qa | PHP/Beget | [architektonica-website-qa](../skills/architektonica-website-qa/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Проверить в WEB: http/формы/навигационные сценарии | HTTP/формы/навигационные сценарии | Матрица URLs и статусов, негативные POST/закрытые пути | Сайт без P0/P1; approval: unverified | READY методика; NOT VERIFIED исполнение | PHP/runtime smoke здесь NOT RUN |
| 06.03 | Проверить desktop, планшеты, iOS и Android. | architektonica-website-qa | mobile-native, break-ui | [architektonica-website-qa](../skills/architektonica-website-qa/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Проверить в WEB: chromium/firefox/webkit и real-device evidence | Chromium/Firefox/WebKit и real-device evidence | Версия/DPR/viewport/state/baseline; iOS/Android отдельно | Сайт без P0/P1; approval: unverified | READY методика; NOT VERIFIED исполнение | Harness/эталонов/устройств нет |
| 06.04 | Проверить доступность, управление с клавиатуры и reduced motion. | architektonica-website-qa | emil-design-eng, mobile-native | [architektonica-website-qa](../skills/architektonica-website-qa/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Проверить в WEB: wcag 2.2 aa журнал | WCAG 2.2 AA журнал | axe + Tab/Escape/focus/reflow + VoiceOver/NVDA; no-JS/reduced-motion | Сайт без P0/P1; approval: unverified | READY методика; NOT VERIFIED исполнение | Ручной и автоматический браузерный аудит NOT RUN |
| 06.05 | Проверить скорость загрузки, стабильность компоновки и плавность сложных сцен. | animation-performance | website-qa, animate | [animation-performance](../skills/animation-performance/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Проверить в WEB: traces/cwv/media/frame-time отчёт | Traces/CWV/media/frame-time отчёт | Лабораторные/полевые p75 раздельно; teardown/offscreen и память | Сайт без P0/P1; approval: unverified | READY методика; NOT VERIFIED исполнение | Замеры на целевых телефонах NOT RUN |
| 06.06 | Проверить безопасность и готовность к публикации. | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Проверить в WEB: релизная проверка безопасности | Релизная проверка безопасности | Контекстное экранирование/приватные файлы/логи; P0/P1 устранены | Сайт без P0/P1; approval: unverified | READY методика; NOT VERIFIED исполнение | Реальный серверный аудит NOT RUN |
| 07.01 | Подготовить production на Beget. | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Выполнить после разрешения запуска: проверенная конфигурация beget | Проверенная конфигурация Beget | Версия/расширения/PHP/Apache; display_errors/debug off | Опубликованный сайт; approval: unverified | READY методика; NOT VERIFIED исполнение | Доступа к production нет |
| 07.02 | Настроить домен, SSL и необходимые серверные параметры. | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Выполнить после разрешения запуска: домен/https/заголовки/rewrite | Домен/HTTPS/заголовки/rewrite | SSL/mixed-content/закрытые файлы/ACME/реальные 301/404/405 | Опубликованный сайт; approval: unverified | READY методика; NOT VERIFIED исполнение | Apache/Beget испытания NOT RUN |
| 07.03 | Проверить формы и уведомления на реальном сервере. | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Выполнить после разрешения запуска: проверенная production-доставка обращений | Проверенная production-доставка обращений | Безопасная тестовая заявка и уведомление; отсутствие дублей | Опубликованный сайт; approval: unverified | READY методика; NOT VERIFIED исполнение | Рабочий backend/контакты/сервер требуются |
| 07.04 | Настроить индексацию, sitemap, robots и аналитику. | architektonica-search-visibility | PHP/Beget, website-qa | [architektonica-search-visibility](../skills/architektonica-search-visibility/SKILL.md); [методика](php-beget-release-checklist.md) | Выполнить после разрешения запуска: проверенная индексация и аналитика | Проверенная индексация и аналитика | Все noindex-слои, robots/sitemap/schema/hreflang/consent/events | Опубликованный сайт; approval: unverified | READY методика; NOT VERIFIED исполнение | Content approval false; запуск запрещён |
| 07.05 | Подготовить резервное копирование и механизм отката. | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Выполнить после разрешения запуска: backup, изолированный restore и rollback | Backup, изолированный restore и rollback | Восстановление выполнено; ответственный/версия; post-rollback smoke | Опубликованный сайт; approval: unverified | READY методика; NOT VERIFIED исполнение | Инфраструктурное упражнение NOT RUN |
| 07.06 | Выполнить финальную приёмку и опубликовать сайт. | architektonica-website-qa | PHP/Beget, critical-editor | [architektonica-website-qa](../skills/architektonica-website-qa/SKILL.md); [методика](php-beget-release-checklist.md) | Выполнить после разрешения запуска: итоговая приёмка и post-deploy smoke | Итоговая приёмка и post-deploy smoke | Владелец разрешил deploy, формы/URL/SEO после выпуска; все NOT RUN видны | Опубликованный сайт; approval: unverified | READY методика; NOT VERIFIED исполнение | Deploy не выполнялся и не разрешён этим аудитом |

Дополнительные обязательные детали задания (не новые этапы):

| Этап | Задача | Ответственный навык | Дополнительные навыки | Источник | Действие агента | Результат | Самопроверка | Gate | Статус | Пробел |
|---|---|---|---|---|---|---|---|---|---|---|
| 03 | Главная/услуга/кейс/статья: отдельная композиция | architektonica-ui-ux-expert | narrative-design, emil-design-eng | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](engine-template-adaptation.md) | Разработать четыре типа блоков под реальные тексты | Типографика, дизайн-токены, состояния и медиа по жанру | Длинный RU/EN текст, 320px, читаемость статьи | Дизайн этапа 03; approval: unverified | PLANNED | Нужны утверждённые образцы |
| 04 | GSAP/ScrollTrigger/Lenis resource lifecycle | animation-performance | animate, mobile-native | [animation-performance](../skills/animation-performance/SKILL.md); [методика](engine-template-adaptation.md) | Проверить ticker/refresh/offscreen/teardown/bfcache | Спецификация и затем lifecycle trace | Нет повторных RAF/listeners/инстансов и роста памяти | Образец этапа 04; approval: unverified | PLANNED | Код и замеры NOT RUN |
| 04 | WebGL context loss и облегчённый вариант | architektonica-ui-ux-expert | animation-performance | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | При выборе WebGL описать restore/dispose и DOM-эквивалент | Статическая композиция и работающий fallback | Смысл/CTA доступны без canvas/JS/движения | Образец этапа 04; approval: unverified | PLANNED | WebGL не обязателен без задачи |
| 05 | Creative → WEB: утверждённый snapshot | architektonica-ui-ux-expert | critical-editor, website-qa | [architektonica-ui-ux-expert](../skills/architektonica-ui-ux-expert/SKILL.md); [методика](agent-expert-stage-protocol.md) | Сопоставить source SHA/approval_ref/ID/locale/URL/блок | Контракт в существующем WEB PR | Diff против источника; смысл не изменён самовольно | Preview этапа 05; approval: unverified | READY методика | Публичные материалы ещё не утверждены |
| 06 | Визуальная регрессия и три browser engine | architektonica-website-qa | mobile-native, break-ui | [architektonica-website-qa](../skills/architektonica-website-qa/SKILL.md); [методика](../skills/architektonica-website-qa/references/QA_CHECKLIST.md) | Настроить Playwright и baselines в WEB | Детерминированные baseline/actual/diff | Chromium/Firefox/WebKit отдельно; устройства дополнительно | QA этапа 06; approval: unverified | PLANNED | Harness отсутствует |
| 07 | Изолированное восстановление и smoke после deploy/rollback | PHP/Beget | website-qa | [PHP/Beget](php-beget-release-checklist.md); [методика](php-beget-release-checklist.md) | Проверить восстановление и повторить релизные сценарии | Журнал restore/rollback с версией и временем | Формы/URL/SEO/security снова проверены | Публикация этапа 07; approval: unverified | NOT VERIFIED | Production доступа нет |

## E. Проверка переходов между этапами

Ручной прогон ситуаций этим агентом в общем контексте; основание — прочитанный протокол и конкретное решение ниже. Это не семь независимых LLM-вызовов. Во всех случаях gate этапа не переутверждён самим агентом.

| Ситуация | Выданное решение | Самопроверка | Статус |
|---|---|---|---|
| A. Сразу анимированная главная, нет принятой IA/текста | «Сейчас могу предложить структуру и отдельно обозначенный исследовательский образец сцены. Его нельзя интегрировать как утверждённую главную. Сначала требуется результат этапа 01; текст и дизайн ещё не приняты». | Нет реализации WEB и ложного gate; C5 сохранён как подготовка | PASS ограничений; независимый запуск NOT RUN |
| B. План принят, этап 01 ещё нет | «План v2 задаёт порядок. Ссылка на утверждённый sitemap и owner_approval_ref отсутствует в доступных источниках: approval: unverified». | Приёмка плана не засчитана за приёмку sitemap | PASS |
| C. Небольшой технический дефект во время другого этапа | Безопасную локальную правку выполнить в пределах запроса и перепроверить. Этот аудит исправил триггер кейса и устаревшую релизную ссылку без запуска нового этапа. | Отдельная ветка, sync, проверки; стадии не переутверждены | PASS фактически выполненного исправления |
| D. Справочник предлагает React/Next | Оставить PHP/HTML/CSS/JS и существующий GSAP; брать общий принцип взаимодействия, не переносить фреймворк. | В diff нет React/Next/новых зависимостей | PASS |
| E. Неподтверждённый результат в кейсе | Удалить утверждение о внедрении/эффекте; сохранить известные архитектуру и прототип; не дописывать клиента. | Контрольный результат C3, Fact Bank §1/§6 | PASS ограничений; публичный кейс PARTIAL |
| F. CI Success, браузерных тестов нет | «Целостность пакета проверена. Визуальная регрессия и доступность NOT RUN». | Здесь даже remote CI не объявлен успешным; 34 unittest/16 node не выданы за browser QA | PASS |
| G. Страница создана без mobile QA | «Страница реализована, мобильная проверка NOT RUN; полностью готовой её не объявляю». | Никакой реальный mobile QA не приписан этому аудиту | PASS решения; реальный браузерный сценарий NOT RUN |

## F. Ошибки и противоречия

| ID | Где | Серьёзность / воспроизводимость | Последствие | Исправление / состояние |
|---|---|---|---|---|
| F1 | `skills/architektonica-portfolio-case-writer/SKILL.md`, «Триггеры» | MEDIUM, прямое чтение: URL перечислен как триггер без контекстного ограничения в самом пункте | Технический запрос может превратиться в написание кейса вопреки AGENTS | Уточнён триггер, обновлено зеркало; первичный источник фактов не менялся |
| F2 | `AGENTS.md`, «Приоритет и маршрут» | LOW, общий канон и фактические категории были описаны в разных местах | Возможна неверная оценка приоритета методики и протокола | Добавлен единый порядок из задания и границы фактологического реестра |
| F3 | `methods/php-beget-release-checklist.md`, последний абзац | LOW, воспроизводимо на base `ea24385`: ожидание уже объединённого PR #12 | Повторная ненужная подготовка или впечатление отсутствия Website QA | Заменено действующими ссылками и разделением серверной/браузерной ответственности |
| F4 | `skills/improve-animations/SKILL.md`, execute; `break-ui`, report-and-stop | MEDIUM, чтение импортированных вариантов | Автоматический review-animations либо лишняя остановка после уже порученного исправления | Оригиналы Emil сохранены; производственная адаптация прямо запрещает обход explicit-only/самовольную делегацию и повторный gate малого исправления |
| F5 | `methods/agent-expert-stage-protocol.md`, передача в WEB | MEDIUM, не было конкретного version/approval/mapping контракта | При реализации может потеряться утверждённый текст или URL | Добавлены source/target SHA, approval_ref, mapping, сверка diff и отдельное согласование смысловых изменений |
| F6 | `methods/skill-effectiveness-evaluation.md` | LOW, требование независимой оценки без оговорки о доступном общем контексте | Самооценку можно ошибочно выдать за полную приёмку | Явно разделены контрольный прогон, чистые контексты, baseline и независимая оценка; обязательная процедура не отменена |
| F7 | WEB `SITE_ROADMAP.md:25–35`, `AGENTS.md` Scope/Work protocol | HIGH для перехода к реализации; таблица ставит креатив 02/UI 04 до финального контента 05, называет себя утверждённым единым планом | Новый агент в WEB может вернуться к прежнему порядку и отдельному стартовому этапу 00 | **Не исправлено в WEB: read-only scope.** Протокол Creative требует сверки и отдельной синхронизации с v2 до зависимой реализации. Этап 01 Creative доступен сейчас |

Ни один дефект не требовал изменения Brand Core, Fact Bank, Services, Case Studies, Copy Registry, защищённого плана v2, девяти оригиналов Emil или сторонних лицензий. Удаление файлов/веток, main merge и production deploy не выполнялись.

## G. Пробелы и необходимость навыков

**Критические для начала этапа 01:** не выявлены после локальных исправлений. Методики IA/контента/UX/motion и проверка целостности готовы. Отсутствие принятого sitemap означает старт этапа 01, не дефект системы.

**Высокий зависимый риск:** F7 требуется закрыть в WEB отдельным разрешённым изменением до реализации по этапам. Не вводить второй план и не менять канон Creative ради старой нумерации WEB.

**Некритические условия приёмки агента:** пять чистых контекстов, baseline при наличии средств, независимый человек с рубрикой 0/1/2; сохранить owner_approval_ref реальных результатов. Контрольные материалы C готовы к такой оценке, не публикуются автоматически. Внешние ссылки/живые кейсы и Notion не прошли новую полную сетевую проверку в этой сессии; локальные ссылки проверены verifier. Исторический статус сайта не равен текущей работе компании.

**Инструментальные задачи WEB:** Playwright-конфигурация и три browser engines, axe и ручные сценарии, real-device лаборатория, реальные эталоны, performance traces/budgets, рабочая форма, измерение lead_confirmed, серверный release/restore/rollback. Их отсутствие ожидаемо до этапов 05–07 и не лечится ещё одним теоретическим навыком.

Для F1/F2/F3/F4 достаточно уточнения существующих инструкций; для F5 — существующего протокола; для F6 — существующей методики оценки; для F7 — согласования документации WEB с принятым v2. Для инфраструктуры нужны инструменты/доступы. **Новый навык не требуется ни для одного обнаруженного пробела.**

## H. Реальные команды и доказательства

| Команда/проверка | Результат | Граница |
|---|---|---|
| `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` и PR #13 head | PASS: получены Creative `ea24385` / WEB `002dfee`; PR #13 содержится в main по Git | Не заменяет API-проверку check/deployment/discussion |
| `python3 scripts/skill_catalog.py --json` | PASS: 21, errors=[]; prototype/review-animations explicit-only | Обнаружение, не активация |
| `python3 scripts/sync_skills.py --check` | PASS: 0 errors | Зеркала/пути |
| `python3 scripts/verify_package.py` | PASS: Skills 21 / baseline 21 / errors 0 | YAML, локальные ссылки/ресурсы, лицензии, каталог, SHA полного плана; не браузер |
| `python3 -m unittest discover -s tests -v` | PASS: 34/34 на Python 3.12.14 | Включая 2 protocol и 2 fixture tests; не генерация LLM |
| Та же проверка через `/tmp/architektonica-ci311/bin/python` | PASS: verifier 0 ошибок, 34/34 | Локальная проверка CI-версии Python 3.11.17 |
| Та же проверка через `/tmp/architektonica-ci313/bin/python` | PASS: verifier 0 ошибок, 34/34 | Локальная проверка CI-версии Python 3.13.5 |
| `python3 -m unittest tests.test_skill_evaluation -v` | PASS: 2/2 | Только структура контрольных заданий и наличие рубрики |
| Поиск Pro Max `scroll trigger cleanup --domain gsap --json` / `dispose context memory --stack threejs --json` | PASS: по 3 записи; для C5 взяты только уместные идеи: не двигать текст, cleanup и dispose | Не применялись автоматически magnetic preset, will-change или WebGL |
| Сравнение JSON Creative и литералов PHP WEB без исполнения PHP | PASS: 81/81, 17/17; полное равенство списка direction/name/scope | Не подтверждает отображение полного каталога в UI |
| WEB `node --test tests/*.test.cjs` | PASS: 16/16, Node 24.19.0 | VM/CSS/JS fixtures, не браузерное QA |
| `git diff --check`; сравнение защищённых источников с base | PASS после итогового прогона | Проверяет границы diff; не подтверждает художественное качество |
| `git merge-base --is-ancestor origin/main HEAD`; `git merge-tree --write-tree origin/main HEAD` | PASS: актуальный main является предком; проверочное объединение без конфликтов | Только проверенная версия Git, без main merge |
| `gh api repos/rafisusmanov/architektonica-creative/pulls/13` | NOT RUN получения данных: API Forbidden | GitHub API отсутствует в effective allowlist; не утверждать зелёный CI |
| PHP lint / WEB `python3 -m unittest discover -s tests -v` | NOT RUN: PHP executable не найден | Не устанавливался ради read-only сверки; CI WEB описывает PHP 8.4/8.5, его live-результат не прочитан |
| Vercel preview, browser regression/axe, real iOS/Android/скринридеры, traces/CWV, Beget/Apache/SSL/restore | NOT RUN: нет подтверждённого preview/эталонов, harness, устройств и production-доступов | Наличие chromium в окружении не заменяет работающий PHP preview и полную матрицу |
| Чистые LLM-контексты, baseline и независимая человеческая оценка | NOT RUN | Прогон C/E — текущий агент/общий контекст |

CI Creative имеет pull_request/push main/audit/**, Python 3.11/3.13; конфигурация прочитана. Live Actions и Vercel build не подтверждены. Проверки не расширяют разрешение на main merge или deploy.

## I. Creative ↔ WEB: что существует

Read-only snapshot WEB: `002dfee`. В `includes/routes.php` реально описаны `/`, `/about`, `/services`, `/project`, `/blog`, `/contact`, коллекции `/services/<slug>`, `/project/<slug>`, `/blog/<slug>`, редиректы и обработка 404. Наличие route/view — не готовая утверждённая страница.

| Область | Фактическое состояние | Следующее действие по v2 |
|---|---|---|
| PHP bootstrap/router/layout, partials/components, Engine CSS/Webflow/GSAP | IMPLEMENTED как техническая основа | Сохранять работающие узлы; retain/rework/extend/replace под принятые материалы |
| Каталог `includes/data/service-catalogue.php` | IMPLEMENTED: полная синхронная копия 17/81 | Подключить к утверждённому UI; сейчас `includes/data/services.php` содержит отдельные демо-карточки |
| About/blog/article/case/service view | IMPLEMENTED шаблоны; готовность контента NOT VERIFIED | Заменять только принятыми материалами, не считать демо публикациями компании |
| `/careers`, отдельный процесс, юридические/служебные страницы, RU/EN | PLANNED; соответствующие маршруты не найдены в текущей route table | Определить состав на этапе 01; реализовать на 05, без фиктивных вакансий |
| Проекты и статьи Engine | В data/templates остались демонстрационные записи; blog author Marvin McKinney и даты Engine | Заменить/скрыть до разрешения индексации; не приписывать их ARCHITEKTONICA |
| Контакты | В config остаются hello@enginestudio.com, demo phone/address | Требуются реальные контакты владельца на этапе содержания/релиза |
| Форма | IMPLEMENTED preview-отказ: JSON 403, иначе 303; сообщения не отправляются/не сохраняются | Реальный приём/доставка/аналитика на этапе 05. Для production это блокер |
| Preview и schema | `content_approved=false`; noindex и JSON-LD gate присутствуют в PHP | Не отключать до принятия фактов/контента и проверки всех слоёв индексации |
| Исполняемые проверки | Python HTTP smoke в tests и GitHub workflow; 16 Node tests локально PASS | Добавить браузерный harness и реальные artefacts по Website QA |
| Клиентский кабинет / будущий консультант | Отдельный проект; место предусмотрено методиками, endpoint не подтверждён | Только согласованные точки входа; никаких вымышленных функций |
| Передача из Creative | Протокол теперь задаёт source SHA/approval_ref → ID/locale/URL/block → target SHA → diff/checks | Выполнять в WEB PR после утверждения материалов; синхронизировать старый WEB roadmap |

WEB не изменён: работа велась с экспортом Git-tree в `/tmp/arch-web-acceptance`, изменения source-веток WEB не создавались. Тестовые кэши в `/tmp` не являются изменением репозитория.

## J. Итоговое решение и первый результат

**READY WITH CONDITIONS.** Можно начинать этап 01: требуемые навыки обнаруживаются, все 21 инструкции прочитаны для аудита, исходники/зеркала/каталог/защищённый план проверены, пять контрольных решений подготовлены, сценарии A–G не переутверждают этапы. Эффективность модели в независимом чистом контексте и оценка человеком остаются неподтверждёнными. Согласование WEB с каноном v2 обязательно до зависимой реализации; браузерные/серверные ворота выполняются на соответствующих этапах.

**Первый конкретный результат владельцу:** полная информационная архитектура RU/EN — sitemap обязательных разделов, 17 направлений/81 услуга и решение о detail_page каждой, предлагаемые стабильные ID/URL, навигационные сценарии, связи услуг/кейсов/статей, статусы публикации/переводов, место кабинета и будущего консультанта. Утверждается этот артефакт целиком; approval_ref сохраняется в существующей задаче/PR. Этот аудит не является самим sitemap и не закрывает этап 01.

Исправления: commit `01c5c68`, 8 файлов; ветка `audit/expert-agent-acceptance-20261031` от `ea24385` отправлена на GitHub. Отдельным документным коммитом записан фактический результат публикации. `gh pr create --base main --head audit/expert-agent-acceptance-20261031 --body-file /tmp/expert-agent-acceptance-pr-body.md` завершился ошибкой `Post https://api.github.com/graphql: Forbidden`; **PR не создан**, удалённый CI не подтверждён. [Готовый diff](https://github.com/rafisusmanov/architektonica-creative/compare/main...audit/expert-agent-acceptance-20261031) и [форма создания PR](https://github.com/rafisusmanov/architektonica-creative/pull/new/audit/expert-agent-acceptance-20261031) доступны владельцу. Main не изменялся; финальное слияние выполняет владелец.

---

# Историческая ревизия до итоговой приёмки

Ниже сохранён прежний снимок аудита. Его числа тестов, выводы о пробелах и статусы PR относятся к той проверке; текущие результаты и ограничения приведены выше. Исторические рекомендации не являются новыми активными поручениями.

# Ревизия Creative Engine — 31.10.2026

Снимок перед исправлениями: Git main `a493195` (после слияния PR #8). Объект этой ревизии — Creative Engine; код ARCHITEKTONICA-WEB не изменяется. Прочитаны все 20 SKILL.md, связанные рецепты и применимые справочники. Базовый verifier сообщал 0 ошибок, 12 тестов проходили, но следующие дефекты воспроизводились.

## Реальные ошибки и обязательные исправления

| Важность | Где и как воспроизвести | Последствие | Исправление / проверка |
|---|---|---|---|
| Высокая | skills/architektonica-ui-ux-expert: неэкранированное двоеточие в description; разобрать YAML | Хост может не загрузить навык | Folded YAML, безопасный парсер, проверки типов и дубликатов ключей |
| Высокая | .agents/skills: разрешить внешний путь с двумя ../ относительно зеркала | Факты и методики недоступны агенту | Генерация зеркал с пересчётом пути; тест против прежнего побайтного копирования |
| Высокая | UI/UX Expert: обязательный вызов review-animations при каждом motion | Нарушение disable-model-invocation | Явная активация только по запросу пользователя; флаги сохраняются и выводятся каталогом |
| Высокая | MASTER, системный промпт, README: разные приоритеты Site Content Plan, Excel и плана в WEB | Агент снова проектирует от слотов или старого аудита PHP | AGENTS — канон общих правил, полный план v2 — канон этапов; MASTER и старые карты обозначены как история |
| Высокая | verify_package: добавить навык без architektonica-префикса либо повредить YAML | Добавление остаётся вне проверки; ложный зелёный CI | Обнаружение всех папок, YAML, всех ресурсов и зеркал; тест с новым навыком и его рецептом |
| Средняя | AGENTS/director/case-writer: передать URL для технической проверки | Вместо задания создаётся портфолио | Маршрут кейса ограничен запросом на оформление портфолио |
| Средняя | search-visibility: разрешена работа только после текста, а план требует участия в IA | Поисковые намерения и адреса появляются поздно | Два режима: архитектура и доработка готового текста |
| Средняя | UI/UX, director, idea-lab, critical-editor: квоты вариантов и порог баллов | Повторное переизобретение одобренного решения и потеря голоса | Квоты стали приёмами по задаче; правка по конкретному дефекту |
| Средняя | methods/copy-workflow и относительные ссылки методик: несуществующий источник услуг/путь к реестру | Агент теряет нужный источник | Реальные пути; проверка локальных Markdown-ссылок и inline-путей |
| Средняя | psycholinguistic-editor, research map, Reference Texts: старые 11 направлений/60 услуг | Ошибочная рамка каталога | Актуальный каталог/нейтральная формулировка, исходный XLSX не изменён |
| Средняя | site-voice-and-consistency: другое написание имени; Language: ссылка на отсутствующие квоты частотности | Расхождение активных редакционных правил | ARCHITEKTONICA, свобода формы при фактической точности |
| Средняя | UI/UX Pro Max: неизвестный домен через Python API | Возвращаются стили с чужой меткой домена | Ошибка неизвестного домена, автопоиск только по поставляемым данным |
| Средняя | Удалить CSV; выполнить search CLI | Пропавший каталог исключается из состава либо ошибка завершает процесс с кодом 0 | Явный curated-состав, проверка всех CSV, ненулевой код ошибки |
| Средняя | Удалить ui-reasoning.csv; вызвать генерацию с persist | Создаётся рекомендация без обязательного источника | Проверка входов до записи; тест отсутствующего и повреждённого CSV |
| Средняя | Смешать --domain/--stack или передать dials без --design-system | Часть намерения молча игнорируется | Ошибка несовместимых аргументов; отдельные CLI-тесты |
| Низкая | Vendor SKILL: пример «full path» относительный; рекламируется отсутствующий google-fonts | Команда не работает из другого cwd или обещает отсутствующие данные | Уточнён cwd/абсолютный путь, описан локальный состав; smoke из временного каталога |

## Что сохранено

17 направлений и 81 услуга; исходные Fact Bank, Case Studies, Brand Core и каталог; оба пользовательских Excel; все 10 исходных авторских навыков, UI/UX Expert и 9 оригинальных веб-навыков с рецептами. MIT-тексты Emil Kowalski и Next Level Builder сохранены. История полезных материалов доступна здесь и в Git; архив не включён в маршрут действующих инструкций. Изменения авторских навыков исправляют маршрут и проверяемые противоречия, а не заменяют их творческий характер.

## Пробелы компетенций и рекомендации владельцу

Это оценка покрытия, а не предложение массово устанавливать навыки. Минимальные критерии добавлены в [методику блоков](engine-template-adaptation.md); наличие этих критериев не означает выполненную проверку сайта.

| Компетенция | Что уже покрыто | Подтверждённый остаточный пробел | Рекомендация |
|---|---|---|---|
| IA / Content Modeling | Director, reader-insight, narrative-design, search-visibility; каталог 17/81 | Нет утверждённой модели связей, URL и статусов всего сайта, результатов tree test | На этапе 01 расширить существующий UI/UX Expert конкретной моделью услуга–направление–кейс–статья; не создавать второй каталог услуг |
| Visual Regression / Cross-Browser QA | Emil и break-ui дают визуальную инспекцию и фикстуры | В Creative Engine нет исполняемого browser harness и базовых снимков утверждённого дизайна | Отдельная задача в WEB на воспроизводимые визуальные сравнения Chromium/Firefox/WebKit и реальные устройства; новый теоретический навык это не заменит |
| Accessibility Engineering | Emil, mobile-native, break-ui и UX-база содержат focus/contrast/ARIA/reduced-motion | Нет доказательств комплексного WCAG 2.2 AA аудита сложных сцен со скринридером | Расширить существующий QA-маршрут матрицей ручных и автоматических проверок, выполнять по конкретным компонентам; не заявлять соответствие до проверки |
| Creative Web Performance | Animate, animation-performance, GSAP/Three.js-данные, mobile-native | Нет согласованных бюджетов сцен и замеров на целевых устройствах; CWV/cleanup не подтверждены | На этапе 04 задать бюджеты, на реализации собрать traces и проверить lifecycle GSAP/Lenis/WebGL; использовать имеющиеся навыки |
| Editorial Web Design | Narrative/copy/UI/UX/Emil, справочники типографики и токенов | Не хватает утверждённых образцов на реальном длинном контенте, а не ещё одной общей инструкции | Создать и принять блоки статьи/кейса/услуги на этапах 02–03; отдельный навык сейчас избыточен |

Новые сторонние навыки и QA-пакеты не установлены. Рекомендовано расширять собственные методики; внешней лицензии для такой редакционной работы не требуется. Для будущего исполняемого QA-инструмента отдельно проверить конкретную версию, лицензию и совместимость с PHP-preview до добавления зависимости. Наличие React-примеров в MIT-справочнике не требует React в публичном сайте.

## Проверки и границы

Локально: verifier, зеркала и 28 unittest; в том числе все 11 поисковых доменов / 6 стеков, запуск CLI из другого cwd, сохранение существующего MASTER/страницы, ошибки данных/метаданных и полный текст плана. План сопоставлен с вложенным заданием: изменён только статус на утверждённую базовую версию; контрольная сумма защищает весь текст, включая этапы 01–07, следующий цикл и согласование.

CI настроен на Python 3.11/3.13 и запускается для PR, main и push в ветки audit/**. Дополнительно локально проверены Python 3.11.17 и 3.13.5 в отдельных окружениях: verifier — 0 ошибок, unittest — 28/28 на каждой версии; ранее проверен Python 3.12.14. Создание PR и чтение результата GitHub Actions требуют доступного API. В этой сессии api.github.com отсутствовал в разрешённых сетевых адресах; подготовлено добавление домена в черновик конфигурации среды. Сохранение черновика не применяет настройку. Успешные локальные команды и отправленный push не считаются подтверждением удалённого CI. NOT RUN: браузерный QA, WCAG-аудит, профилирование/CWV и PHP сайта (WEB вне текущего задания), новая live-сверка Notion, независимое воспроизведение исследований и проверка актуальных security advisories зависимостей.

Автоматическая проверка ищет буквальные локальные Markdown-ссылки и inline-пути к ресурсам; не проверяет внешние URL, произвольные команды в примерах, семантику всех текстов или наличие фоновой памяти. Семантические противоречия проверены редакционно; этот результат не следует объявлять математической гарантией отсутствия любых будущих конфликтов.

---

## Исторический аудит материалов портфолио

> Историческая запись аудита комплекта. Числа навыков и прежние маршруты ниже описывают тот снимок; актуальные инструкции — [AGENTS.md](../AGENTS.md), реальный каталог — вывод `python3 scripts/skill_catalog.py` из корня. Фактические досье и полезные примеры сохраняются.

# Аудит исходных материалов для сценария «описал работу → получил кейс»

## Что проверено

Проверены входные Markdown-документы, текущие девять навыков, инструкции и демонстрационный кейс W4.11. Пакет дополняется отдельным навыком Portfolio Case Writer. Два исходных Excel (`references/research` и `references/template`) хранятся как неизменённые первичные файлы; они не являются источником доказанных результатов конкретных клиентских проектов.

## Материалы и назначение

- `references/project/02_Architektonica_Fact_Bank.md` — источник статусов, названий, доступной атрибуции, подтверждений, публичных URL и оговорок.
- `references/project/03_Architektonica_Case_Studies.md` — развернутые описания известных работ; интерпретации задачи и напряжения **не являются прямыми цитатами клиента**.
- `references/project/01_Architektonica_Brand_Core.md`, `../references/project/00_Creative_Platform.md`, `../references/project/05_Architektonica_Language.md`, `../references/project/06_Architektonica_Reference_Texts.md` — смысл, редакционный голос и примеры, но не приговор в отношении формата каждого нового кейса.
- `../references/project/04_Architektonica_Services.md` + `../references/project/Услуги_дополнительный_перечень.md` — предлагаемые услуги; наличие в каталоге не доказывает выполненный проект.
- `references/research/*.xlsx`, `methods/research-evidence-map.md` — подсказки по восприятию текста, а не источники выдуманной конверсии.
- `references/template/*.xlsx` — карта полей существующего шаблона, не ограничение на длину или форму кейса.

## Критичные соответствия

- W4.11 «Арктическая Венеция»: в Case Studies есть достопримечательности, сотрудники, природный парк, HR-механика «получить гражданство», digital-открытка. Метрик продаж или трафика там нет.
- W4.07 «Сторис»: сюжет пяти историй опирается на Case Studies, но любые дополнительные функции и эффекты нельзя домысливать.
- W1-A1/W1-A2 Synapto: **спроектированы архитектуры**; W1-P — **интерфейсный прототип**; предложенный пилот — **не реализованный пилот**.
- Для W4 состав участия нередко неполный. При новом описании пользователя используем его точную роль, а не расширяем до «компания реализовала всё».
- Проекты, о которых пользователь сообщает впервые, могут не иметь записи в Fact Bank; не блокировать работу из-за отсутствия ID.

## Что было недостатком исходной версии

Набор умел писать кейсы по существующему досье, но не имел отдельного триггера на «я сделал сайт / снял видео / разработал программу / приложение» и устойчивого формата публикационного пакета. Теперь приоритетный маршрут: `portfolio-case-writer` → `idea-lab` → `narrative-design` → `copy-studio` → `critical-editor` → `search-visibility` (этапы могут проходить незаметно для пользователя).

## Правило для новых материалов

Свободный текст пользователя — первичный источник. Скриншоты, ссылки, репозитории, файлы использовать, если они действительно доступны. При неполной информации сразу писать доступную безопасную первую версию; вопросы задавать лишь дополнительно, когда они существенно улучшают фактологию. Не превращать пометки редактора в содержимое публикуемой страницы.
