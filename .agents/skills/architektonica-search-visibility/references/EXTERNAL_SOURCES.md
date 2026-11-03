# Search Visibility — точные внешние источники и ограничения интеграции

**Принцип:** взяты *методические идеи*, описанные заново для ARCHITEKTONICA. Ни сторонние `SKILL.md`, ни скрипты, ни рантаймы, ни рабочие процессы, ни шаблоны отчетов **не копировались и не устанавливались**. Дополнительного постоянно активного навыка нет.

## Aaron He Zhu — актуальная ветка

- Исходный запрошенный репозиторий: [seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills/tree/3a1578a63cdde8037ee16d32a3ea9f808eae6bd0). Его текущий `main` — **signpost**, прежние 20 навыков заморожены в `v9.9.12`.
- Актуальная разработка: [aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills/tree/903d6479165fe11fc32e73e0e3c8c0179ed0c55a), **commit `903d6479165fe11fc32e73e0e3c8c0179ed0c55a`**, проверено 01.11.2026.
- Лицензия исходного репозитория: [Apache-2.0](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/LICENSE); проверенные выбранные `SKILL.md` объявляют `license: Apache-2.0`. При будущем прямом переносе текста/кода соблюдать LICENSE и атрибуцию.

| Выбранный навык (закреплённая версия) | Путь | Что именно адаптировано |
|---|---|---|
| [keyword-research](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/survey/keyword-research/SKILL.md) | `seo-geo/survey/keyword-research/SKILL.md` | Семантический спрос, источник/дата/регион, unknown-вместо догадок; без обязательных числовых score |
| [serp-analysis](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/survey/serp-analysis/SKILL.md) | `seo-geo/survey/serp-analysis/SKILL.md` | SERP-снимки с локалью, датой, intent и раздельной оценкой search/AI |
| [site-structure-optimizer](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/tune/site-structure-optimizer/SKILL.md) | `seo-geo/tune/site-structure-optimizer/SKILL.md` | URL и link graph, orphan pages, каноническая страница под намерение |
| [geo-content-optimizer](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/implement/geo-content-optimizer/SKILL.md) | `seo-geo/implement/geo-content-optimizer/SKILL.md` | Ответы и извлекаемые факты, разделение readiness/реального цитирования |
| [content-quality-auditor](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/tune/content-quality-auditor/SKILL.md) | `seo-geo/tune/content-quality-auditor/SKILL.md` | Протокол доказательств, unknown и ограничений публикации; 80-пунктовый scorer не импортирован |
| [serp-markup-builder](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/implement/serp-markup-builder/SKILL.md) | `seo-geo/implement/serp-markup-builder/SKILL.md` | Точный SEO-пакет и проверяемая Schema.org на этапе внедрения |
| [technical-seo-checker](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/tune/technical-seo-checker/SKILL.md) | `seo-geo/tune/technical-seo-checker/SKILL.md` | Crawl/index/robots/canonical/hreflang и отдельный технический QA |
| [on-page-seo-checker](https://github.com/aaron-he-zhu/aaron-marketing-skills/blob/903d6479165fe11fc32e73e0e3c8c0179ed0c55a/seo-geo/tune/on-page-seo-checker/SKILL.md) | `seo-geo/tune/on-page-seo-checker/SKILL.md` | Проверка заголовков и метаданных при наличии фактического URL |

Внешние `CORE-EEAT` (80 пунктов) и `CITE` (40) — собственные системы оценивания автора. **Не** официальные факторы ранжирования Google, не внедрены как валидаторы или обязательные числовые пороги. Внешние `memory/`, хранилище результатов, подключаемые API, скрипты Google Autocomplete/Firecrawl/Tavily, scorer и установка `npx skills add` **не включены**. Использовать только после отдельной проверки инструментов и правил безопасности, если появится доказанная потребность.

## SNLabat — единый аудиторский обзор

- Репозиторий: [SEO-GEO-AEO-Skill](https://github.com/SNLabat/SEO-GEO-AEO-Skill/tree/a2c8769b85813912b2b01cd12c3484f061b439fc), **commit `a2c8769b85813912b2b01cd12c3484f061b439fc`**, проверено 01.11.2026.
- Исходный [SKILL.md](https://github.com/SNLabat/SEO-GEO-AEO-Skill/blob/a2c8769b85813912b2b01cd12c3484f061b439fc/SKILL.md) и [README.md](https://github.com/SNLabat/SEO-GEO-AEO-Skill/blob/a2c8769b85813912b2b01cd12c3484f061b439fc/README.md). В просмотренном дереве `main` **нет `LICENSE` или иной явной лицензии** — права на прямое копирование не подтверждены.
- **Адаптирована только идея** трёхслойной проверки сайта: SEO — технические и контентные сигналы; GEO — сущности, доказательства и ясные определения; AEO — естественные вопросы и доступные ответы. Никаких исходных отчётных шаблонов/контента и кода не перенесено.
- Исключены обязательное предварительное уточнение Quick/Full, искусственные оценки /10, нормативные числа слов/символов, навязанный DOCX/PDF и неоправданные предположения о FAQ/HowTo rich results.

## Внутренние ограничения и приоритет

Актуальные решения владельца, Brand Core / Fact Bank / Case Studies, утверждённый план v2 и `AGENTS.md` выше этих источников. В существующем навыке `architektonica-search-visibility` — **единая точка входа**; для отдельной задачи читать только нужный локальный рецепт. Вся аналитика и индексация сайта требуют инструмента и факта проверки; зелёный CI Creative проверяет **методики**, но не доказывает видимость сайта в поиске.
