# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Type

Static HTML project page for the Flow Maps research paper. No build system - just HTML, CSS, and JavaScript served directly.

## Preview Command

```bash
python -m http.server 8000
# Then open http://localhost:8000
```

Or open `index.html` directly in a browser.

## Architecture

**Single-page application** with:
- Bulma CSS framework (in `static/css/`)
- jQuery for DOM manipulation
- Bulma-carousel and bulma-slider plugins
- Font Awesome and Academicons for icons

**Direct editing workflow**: Edit `index.html`, refresh browser. No compilation step.

## Content Customization

Search for `<!-- TODO: ... -->` comments in `index.html` to find all customization points:

- **Metadata** (lines ~5-12): Title, description, keywords
- **Authors** (lines ~78-95): Names, homepages, affiliations
- **Links** (lines ~98-148): arXiv, PDF, code, dataset URLs
- **Abstract** (lines ~210-222): Paper abstract
- **BibTeX** (lines ~353-359): Citation

## Media Assets

**Current state**:
- ✓ Interpolation frames: 240 frames in `static/interpolation/stacked/` (000000.jpg to 000239.jpg)
- ✗ Videos: Need to add to `static/videos/`:
  - `teaser.mp4` - main teaser
  - `result1.mp4`, `result2.mp4`, `result3.mp4` - results carousel
  - `method.mp4`, `results.mp4` - method/results sections

**Optional**:
- Start/end images for interpolation: `static/images/interpolate_start.jpg`, `interpolate_end.jpg`

## Interactive Components

**Interpolation Slider** (`static/js/index.js`):
- Preloads 240 frames on page load (line 4: `NUM_INTERP_FRAMES`)
- Controlled by slider input (lines 70-74)
- Update frame count by changing `NUM_INTERP_FRAMES` if regenerating interpolation

**Video Carousel** (lines ~174-200 in HTML):
- Auto-initializes via bulma-carousel plugin
- Configuration in `static/js/index.js` lines 32-42 (slides per view, autoplay, etc.)
- Add/remove videos by duplicating `.item` divs in HTML

## Removing Sections

To remove unused sections, delete entire blocks:
- Results carousel: lines ~174-200
- Method/Results columns: lines ~247-279
- Interpolation slider: lines ~281-322
- Related links: lines ~325-344

Page will reflow automatically.

## File Structure

```
index.html              # Main page (edit this)
static/
├── css/               # Bulma framework (don't edit)
├── js/
│   └── index.js       # Custom interactions (edit for frame count, carousel config)
├── images/            # Static images
├── videos/            # MP4 files (add yours here)
└── interpolation/
    └── stacked/       # 240 interpolation frames (already populated)
```

## Important Notes

- Line numbers are approximate and shift as content changes
- Based on Nerfies project page template - keep footer attribution (CC BY-SA 4.0)
- Videos won't display until files exist in `static/videos/`
