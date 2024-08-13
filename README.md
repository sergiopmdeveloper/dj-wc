# dj-wc

Django Template based on the use of web components with Lit 🖥️✨

## Installation

1. Clone the project and navigate to the folder:
```bash
    git clone https://github.com/sergiopmdeveloper/dj-wc.git
    cd dj-wc
```

2. Configure git hooks:
```bash
    chmod +x .githooks/pre-commit
    git config core.hooksPath .githooks
```

3. Install Python dependencies:
```bash
    pip install -r requirements-dev.txt
```

4. Install Node.js dependencies of the frontend module:
```bash
    cd frontend
    npm install
```

## Run Locally

1. Start the Django development server:
```bash
    python manage.py runserver
```

2. Start the frontend development server:
```bash
    npm run watch
```

## Tech Stack

**Frontend:** Lit, Webpack

**Backend:** Django

## Authors

- [@sergiopmdeveloper](https://www.github.com/sergiopmdeveloper)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](https://choosealicense.com/licenses/mit/)
