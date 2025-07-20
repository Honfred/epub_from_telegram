import yaml
from downloader import fetch_telegraph_links
from telegraph_parser import parse_telegraph_article
from epub_builder import create_epub

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    telegram_cfg = config['telegram']
    book_cfg = config['book']

    print('🔍 Сканируем Telegram-канал...')
    all_links = fetch_telegraph_links(
        api_id=telegram_cfg['api_id'],
        api_hash=telegram_cfg['api_hash'],
        channel_username=telegram_cfg['channel_username']
    )

    try:
        last_index = all_links.index(telegram_cfg['last_read_link'])
        links = all_links[:last_index]
    except ValueError:
        print('❌ Последняя прочитанная глава не найдена.')
        return

    links.reverse()
    print(f'📚 Глав для скачивания: {len(links)}')

    chapters_data = []

    for idx, link in enumerate(links, 1):
        print(f'📥 Глава {idx}: {link}')
        try:
            title, content_html = parse_telegraph_article(link)
            chapters_data.append((title, content_html))
        except RuntimeError as e:
            print(f'⛔ Ошибка: {e}')
            return

    create_epub(
        book_title=book_cfg['title'],
        book_author=book_cfg['author'],
        chapters_data=chapters_data,
        output_filename=book_cfg['output_filename']
    )

if __name__ == '__main__':
    main()
