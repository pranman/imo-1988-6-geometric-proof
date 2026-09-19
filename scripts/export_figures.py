#!/usr/bin/env python3
"""Export the exact README SVG artwork as vector PDFs for LaTeX."""

from pathlib import Path

from cairosvg.surface import PDFSurface, cairo

ROOT = Path(__file__).resolve().parents[1]


class CompatiblePDFSurface(PDFSurface):
    """Keep the exports compatible with LaTeX engines that default to PDF 1.5."""

    def _create_surface(self, width, height):
        surface, width, height = super()._create_surface(width, height)
        surface.restrict_to_version(cairo.PDF_VERSION_1_5)
        return surface, width, height


def main():
    for source in sorted((ROOT / "figures").glob("*.svg")):
        target = source.with_suffix(".pdf")
        CompatiblePDFSurface.convert(url=str(source), write_to=str(target))
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
