"""TideLink command-line client.

Uses the bundled zero-dependency ``tidelink`` module.

Set your key first:
    export TIDELINK_API_KEY=YOUR_KEY
Get a free key: https://tidelink.xyz/dashboard.html
"""
import os
import sys
import argparse

from tidelink import TideLink


def main(argv=None):
    ap = argparse.ArgumentParser(prog="tidelink-cli", description="TideLink LLM CLI")
    ap.add_argument("--key", default=os.environ.get("TIDELINK_API_KEY"),
                    help="TideLink API key (or set TIDELINK_API_KEY)")
    ap.add_argument("--model", default="glm-4-flash", help="Model id (placeholder ok)")
    ap.add_argument("message", help="The message to send")
    args = ap.parse_args(argv)

    if not args.key:
        print("Error: set TIDELINK_API_KEY or pass --key", file=sys.stderr)
        return 1

    tl = TideLink(args.key)
    r = tl.chat([{"role": "user", "content": args.message}], model=args.model)
    print(r["choices"][0]["message"]["content"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
