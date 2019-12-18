from pathlib import Path
import aiohttp

def prompt(query: str) -> bool:
    options = ["y", "n"]
    check = input(f"{query} ").lower()
    if check not in options:
        return ValueError
    elif check == "y":
        return True
    else:
        return False


async def get_latest_sha1():
    url = "https://api.github.com/repos/JohnRipper/QuantumJump/commits"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            gitjson = await response.json()
            sha1 = gitjson[0]["sha"][:7]
            return sha1


def get_current_sha1():
    cwd = Path.cwd()
    headfile = Path(cwd / ".git/refs/heads/master")
    sha1 = "-Not in a git repository-"
    if headfile.exists():
        sha1 = headfile.read_text()[:7]
    return sha1
