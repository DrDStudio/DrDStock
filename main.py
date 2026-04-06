name: Daily Stock Update

on:
  workflow_dispatch: # Cái này giúp xuất hiện nút bấm chạy tay

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install vnstock google-generativeai pandas
      - name: Run bot
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python main.py
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
          publish_branch: gh-pages
