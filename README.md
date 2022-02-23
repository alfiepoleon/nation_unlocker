# Nation unlocker

This is a simple project created with `Python, flask` and `BeautifulSoup4`

It fetches an article from [Nation Kenya](nation.africa) and removes the registration requirement as well as the ads.

Due to **CORS**, images are not displayed

It is made possible because they use classes to hide content from unregistered users, so removing those classes and changing some css unlocks everything.

To have the article saved in `res` folder as `article.html` uncomment the following in `main.py`
```python
 with open("res/article.html", "w", encoding='utf-8') as file:
         file.write(soup_str)
```
## Running
1. Create and activate a python3 virtual env.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install pip packages
    ```bash
    pip install -r requirements.txt
    ```

3. Run it
    ```bash
    python main.py
    ```