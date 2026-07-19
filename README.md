# GCP Icons

![GitHub Pages](https://github.com/jajera/gcp-icons/actions/workflows/pages.yml/badge.svg)

A searchable web library for browsing and copying official Google Cloud product
icons. It includes the current category and core-product sets alongside the
legacy console icon collection.

## Features

- Search by product name, tags, or common abbreviations
- Filter current category, core product, and legacy icon sets
- Copy SVG or PNG data to the clipboard
- Download icons as SVG or PNG
- Light and dark themes
- Responsive layout for desktop and mobile
- Shareable search and tag filters in the URL

## Statistics

- **261** total icons
  - **26** current category icons
  - **19** current core product icons
  - **216** legacy console icons

## Usage

Serve the repository from a local web server:

```shell
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

Use the search box or tags to find an icon. Hover over a card to copy or
download its SVG or PNG representation.

## Repository structure

```text
icons/
  category/  Current Google Cloud category icons
  product/   Current Google Cloud core product icons
  legacy/    Legacy Google Cloud console icons
icons.json   Searchable icon metadata used by the web app
scripts/     Metadata generation tooling
```

Regenerate `icons.json` after adding or renaming an icon:

```shell
python3 scripts/generate_icons_json.py
```

## Attribution

Icon assets are provided by the
[Google Cloud icon library](https://cloud.google.com/icons). Google Cloud and
related marks are trademarks of Google LLC. Refer to Google's icon and brand
guidance before redistributing or modifying the assets.

## License

The website code is available under the [MIT License](LICENSE). Google Cloud
icon assets remain subject to Google's applicable terms and are not relicensed
under MIT.
