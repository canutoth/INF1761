import argparse
import pathlib
import sys
from urllib.parse import urlparse
import segno

def valid_url(s: str) -> str:
    u = urlparse(s)
    if u.scheme not in ("http", "https") or not u.netloc:
        raise argparse.ArgumentTypeError("URL must start with http:// or https:// and include a host")
    return s

def main() -> None:
    p = argparse.ArgumentParser(description="Generate a non-expiring static QR code from a URL.")
    p.add_argument("url", type=valid_url, help="The URL to encode")
    p.add_argument("-o", "--out", default=None,
                   help="Output path. Extension decides the format. Defaults to qr-<host>.png")
    p.add_argument("--format", choices=["png", "svg", "pdf", "eps"], default=None,
                   help="Force format if --out has no extension")
    p.add_argument("--ec", choices=list("LMQH"), default="H",
                   help="Error correction level. H is most robust")
    p.add_argument("--scale", type=int, default=10,
                   help="Module size in pixels for raster formats like PNG")
    p.add_argument("--border", type=int, default=4,
                   help="Quiet zone width in modules. Keep at least 4")
    args = p.parse_args()

    qr = segno.make(args.url, error=args.ec)

    if args.out:
        outpath = pathlib.Path(args.out)
        ext = outpath.suffix[1:].lower() if outpath.suffix else (args.format or "png")
        if not outpath.suffix:
            outpath = outpath.with_suffix("." + ext)
    else:
        host = urlparse(args.url).netloc.replace(":", "-")
        ext = "png"
        outpath = pathlib.Path(f"qr-{host}.{ext}")

    if ext == "png":
        qr.save(outpath, scale=args.scale, border=args.border)  # raster
    elif ext in ("svg", "pdf", "eps"):
        qr.save(outpath, border=args.border)  # vector for print
    else:
        sys.exit(f"Unsupported format: {ext}")

    print(f"Wrote {outpath.resolve()}")

if __name__ == "__main__":
    main()
