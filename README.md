# Research Project Page Template

A clean, professional template for academic research project pages. Based on the [Nerfies project page](https://nerfies.github.io).

## Features

- **Responsive design** using Bulma CSS framework
- **Interactive elements**: video carousel, image interpolation slider
- **Academic formatting**: paper links, BibTeX citation, author affiliations
- **Easy customization**: all content marked with clear TODO comments

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/project-page-template.git
   cd project-page-template
   ```

2. **Edit `index.html`** - Search for `TODO` comments and replace with your content:
   - Page metadata (title, description, keywords)
   - Author information and affiliations
   - Paper links (arXiv, PDF, code, dataset)
   - Abstract text
   - BibTeX citation

3. **Add your media files**:
   - Videos: Place MP4 files in `static/videos/`
   - Images: Place images in `static/images/`
   - Interpolation frames (optional): Place in `static/interpolation/stacked/`

4. **Preview locally**:
   ```bash
   python -m http.server 8000
   # Navigate to http://localhost:8000
   ```

5. **Deploy** to GitHub Pages, Netlify, or your preferred hosting

## Customization Guide

### Required Updates

- **Title & Metadata** (lines 5-12): Update page title, description, and keywords
- **Authors** (lines 78-95): Replace with your authors and affiliations
- **Links** (lines 97-148): Update arXiv, PDF, code, and dataset URLs
- **Abstract** (lines 210-222): Replace with your paper abstract
- **BibTeX** (lines 353-359): Update citation information

### Media Files

- **Teaser video**: `static/videos/teaser.mp4` - Main demonstration video
- **Results videos**: `static/videos/result1.mp4`, `result2.mp4`, `result3.mp4` for carousel
- **Method/Results videos**: Add as needed for additional sections
- **Interpolation** (optional):
  - Add frames to `static/interpolation/stacked/000000.jpg` through `000239.jpg`
  - Update frame count in `static/js/index.js` (line 4)
  - Add start/end images: `static/images/interpolate_start.jpg` and `interpolate_end.jpg`

### Optional Sections

You can remove or customize these sections in `index.html`:

- **Results carousel** (lines 174-200): Remove if not needed
- **Method/Results columns** (lines 247-279): Customize or remove
- **Interpolation slider** (lines 281-322): Remove if not using
- **Related Links** (lines 325-344): Update with your related work

## File Structure

```
.
├── index.html              # Main page (edit this!)
├── static/
│   ├── css/               # Bulma framework and custom styles
│   ├── js/                # Interactive components
│   ├── images/            # Static images
│   ├── videos/            # Video demos (add your files here)
│   └── interpolation/     # Interpolation frames (optional)
│       └── stacked/
├── CLAUDE.md              # AI assistant instructions
└── README.md              # This file
```

## Credits

This template is based on the [Nerfies project page](https://nerfies.github.io) by Keunhong Park and colleagues.

If you use this template, please:
- Keep the footer attribution to the Nerfies project
- Consider starring this repository

## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>

This template is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
