# 🤝 Contributing

Thanks for your interest in contributing!

---

## Quick Start

1. Fork the repo
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ai-digest-phone-calls.git`
3. Create a branch: `git checkout -b feature/my-feature`
4. Make changes
5. Test: `python -m src.main test`
6. Push: `git push origin feature/my-feature`
7. Open Pull Request

---

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add testing dependencies
pip install pytest black flake8
```

---

## Code Style

- Python 3.9+
- Follow PEP 8
- Use descriptive variable names
- Add docstrings to functions

Quick format:
```bash
black src/
flake8 src/
```

---

## Areas for Contribution

### Easy
- [ ] Add more news sources to `config/news_sources.py`
- [ ] Improve documentation
- [ ] Fix typos
- [ ] Add comments to confusing code

### Medium
- [ ] Add email notification option
- [ ] Add Slack integration
- [ ] Support for Discord
- [ ] Better error handling

### Hard
- [ ] Add web dashboard for config
- [ ] Support multiple schedules per day
- [ ] Add custom digest templates
- [ ] Database logging

---

## Testing

```bash
# Test a single component
python -m src.news_scraper
python -m src.digest_generator
python -m src.tts_converter
python -m src.caller

# Full test
python -m src.main test

# Show config
python -m src.main show-config

# List sources
python -m src.main list-sources
```

---

## Pull Request Process

1. Update CHANGELOG.md with your changes
2. Ensure tests pass
3. Add docstrings if adding functions
4. Reference any related issues (#123)
5. Describe what your PR does

Example PR title:
- `Add Reddit news source`
- `Fix Twilio auth error`
- `Improve error messages`

---

## Questions?

Open an issue or discussion. We're friendly! 😊

---

## License

By contributing, you agree your code will be under MIT License.
