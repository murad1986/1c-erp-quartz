#!/bin/bash
# Синхронизация контента из Obsidian vault → Quartz
# Запускать после обновления уроков в vault

VAULT="/Users/muradnurmagomedov/Library/Mobile Documents/iCloud~md~obsidian/Documents/Zettelkasten/education/1c_erp_qcom"
QUARTZ="$(dirname "$0")/content"

for w in week_1 week_2 week_3 week_4 week_5 week_6 week_7 week_8; do
  rsync -a --delete \
    --exclude="lesson_writer_agent.md" \
    --exclude="promise_registry.md" \
    --exclude="case_registry.md" \
    --exclude="visual_prompts.md" \
    --exclude=".DS_Store" \
    --exclude="_meta" \
    "$VAULT/$w/" "$QUARTZ/$w/"
done

cp "$VAULT/README.md" "$QUARTZ/README.md"
echo "✅ Контент синхронизирован"
echo "Запусти: npx quartz build --serve — для превью"
echo "Для деплоя: git add -A && git commit -m 'update content' && git push"
