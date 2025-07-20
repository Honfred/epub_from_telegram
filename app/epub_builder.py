from ebooklib import epub

def create_epub(book_title, book_author, chapters_data, output_filename):
    book = epub.EpubBook()
    book.set_title(book_title)
    book.add_author(book_author)

    chapters = []

    for idx, (title, html) in enumerate(chapters_data, 1):
        chapter = epub.EpubHtml(title=title, file_name=f'chap_{idx}.xhtml', lang='ru')
        chapter.set_content(f'<h1>{title}</h1>{html}')
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = chapters
    book.spine = ['nav'] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(output_filename, book)
    print(f'\n✅ EPUB-файл сохранён: {output_filename}')
