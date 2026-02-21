def test_page_load(page):
    print("Page Title:", page.title())
    assert page.title() is not None
