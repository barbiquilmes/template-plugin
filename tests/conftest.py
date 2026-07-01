"""
Stub out the `mcp` package so tests can import server.py without the plugin venv.
The business logic inside describe_csv_file has no runtime dependency on mcp;
the decorator @mcp.tool() is just registration that happens at import time.
"""
import sys
from unittest.mock import MagicMock

# Build a fake mcp hierarchy before server.py is imported
_mcp_mock = MagicMock()
_mcp_mock.server.fastmcp.FastMCP.return_value.tool.return_value = lambda f: f

sys.modules.setdefault("mcp", _mcp_mock)
sys.modules.setdefault("mcp.server", _mcp_mock.server)
sys.modules.setdefault("mcp.server.fastmcp", _mcp_mock.server.fastmcp)
