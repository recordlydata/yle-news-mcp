# Yle News MCP Server

A Model Context Protocol (MCP) server for fetching news from Yle RSS feeds.

![image](https://github.com/user-attachments/assets/f010d5b7-fb37-4257-96dd-d7a9dc0c1cba)

## Features

- Fetch news from various Yle RSS feeds
- Support for multiple topics (news, recent, most_read, kotimaa, ulkomaat, etc.)
- Sort news items by publication date
- Easy integration with Claude Desktop

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd model-control-protocol-demo
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e ".[test]"
```

## Adding to Claude Desktop

To add this server to Claude Desktop:

1. Open the Claude Desktop configuration file:
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Add the following configuration:
```json
{
    "mcpServers": {
        "yle-news": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/model-control-protocol-demo",
                "run",
                "python",
                "-m",
                "mcp_demo.main"
            ]
        }
    }
}
```

3. Replace `/ABSOLUTE/PATH/TO/model-control-protocol-demo` with the actual absolute path to your project directory.

4. Save the file and restart Claude Desktop.

## Using the Inspector

To debug and test the server using the MCP Inspector:

1. Make sure the virtual environment is activated:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Start the inspector with the server:
```bash
npx @modelcontextprotocol/inspector python -m mcp_demo.main
```

3. The inspector will start and provide a web interface at http://127.0.0.1:6274

4. You can use the inspector to:
   - View available tools
   - Test tool calls
   - Monitor server responses
   - Debug any issues

## Running Tests

To run the test suite:

1. Make sure the virtual environment is activated:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Run the tests:
```bash
pytest -v tests/
```

The test suite includes:
- Testing valid topic fetching
- Testing invalid topic handling
- Testing limit parameter
- Testing all available topics
- Testing date sorting functionality

## Available Topics

The server supports the following topics:
- news: Major headlines
- recent: Recent news
- most_read: Most read articles
- kotimaa: Domestic news
- ulkomaat: Foreign news
- talous: Economy
- politiikka: Politics
- kulttuuri: Culture
- viihde: Entertainment
- tiede: Science
- luonto: Nature
- terveys: Health
- media: Media news
- liikenne: Traffic
- näkökulmat: Perspectives
- urheilu: Sports
- selkouutiset: Easy-to-read news
- english: English news
- sapmi: Sámi news
- novosti: Russian news
- karjalakse: Karelian news

## Development

### Project Structure

```
model-control-protocol-demo/
├── pyproject.toml
├── README.md
├── src/
│   └── mcp_demo/
│       ├── __init__.py
│       ├── main.py
│       └── server.py
└── tests/
    └── test_server.py
```

### Adding New Features

1. Add new RSS feed URLs to the `RSS_FEEDS` dictionary in `server.py`
2. Update the `get_news` function's topic description
3. Add corresponding test cases in `test_server.py`
4. Run the test suite to verify changes

## License

MIT
