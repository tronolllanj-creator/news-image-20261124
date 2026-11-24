import os

def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    magic = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(magic):
        raise SystemExit("entry.png does not start with PNG magic bytes")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        size = len(f.read())
    print(dst)
    print(size)

if __name__ == "__main__":
    main()
