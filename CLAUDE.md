# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Type

This is a **static HTML template** for academic research project pages. There is no build system, package manager, or backend - just HTML, CSS, and JavaScript files that can be opened directly in a browser.

## Preview Command

```bash
python -m http.server 8000
# Then open http://localhost:8000
```

Or simply open `index.html` directly in a browser (some features work better with a local server).

## Architecture

**Single-page HTML application** (`index.html`) with:
- Bulma CSS framework (already included in `static/css/`)
- jQuery for DOM manipulation
- Bulma-carousel and bulma-slider plugins for interactive components
- Font Awesome and Academicons for icons

**No build process** - edit HTML directly and refresh browser.

## Customization Workflow

All customization points are marked with `<!-- TODO: ... -->` comments in `index.html`. When helping users customize:

1. **Search for "TODO"** in index.html to find all placeholder content
2. **Key sections** to update (in order):
   - Metadata: lines 4-11 (title, description, keywords)
   - Authors/affiliations: lines 77-94
   - Paper links: lines 97-148 (arXiv, PDF, code, data)
   - Abstract: lines 210-222
   - BibTeX: lines 353-359
   - Footer: lines 367-374

3. **Media files** users need to add:
   - `static/videos/teaser.mp4` - main demo video
   - `static/videos/result1.mp4`, `result2.mp4`, `result3.mp4` - carousel
   - `static/videos/method.mp4`, `results.mp4` - additional sections
   - Optional: interpolation frames in `static/interpolation/stacked/` (000000.jpg through 000239.jpg)
   - Optional: `static/images/interpolate_start.jpg` and `interpolate_end.jpg`

4. **Sections users may want to remove**:
   - Results carousel: lines 174-200
   - Method/Results columns: lines 247-279
   - Interpolation slider: lines 281-322
   - Related Links: lines 325-344

## Interactive Features

**Image Interpolation Slider** (optional feature):
- JavaScript: `static/js/index.js` lines 3-13, 68-74
- Expects frames in `static/interpolation/stacked/` numbered 000000.jpg to 000239.jpg
- Frame count configurable via `NUM_INTERP_FRAMES` variable (line 4 of index.js)
- If users don't need this, they can delete the entire interpolation section from HTML

**Video Carousel**:
- Uses bulma-carousel plugin (already loaded)
- Automatically initializes on page load
- Add/remove carousel items by editing the HTML (lines 179-196)

## Common Tasks

**Add a new video to carousel**: Copy one of the `.item` divs (lines 179-184) and update the video source and ID.

**Change number of interpolation frames**: Edit `NUM_INTERP_FRAMES` in `static/js/index.js` line 4.

**Remove a section**: Delete the entire `<section>` or `<div class="columns">` block. The page will automatically reflow.

**Add Google Analytics**: Users can add their tracking code at line 13 where the TODO comment is.

## File Organization

```
index.html              # Main page - only file users need to edit
static/
├── css/               # Framework files - don't modify
├── js/                # Plugins + custom code - only edit index.js
├── images/            # User adds their images here
├── videos/            # User adds their videos here (currently empty)
└── interpolation/     # Optional: user adds frame sequences here
    └── stacked/
```

## Important Notes

- **No dependencies to install** - everything is self-contained
- **Line numbers** in comments are approximate and may shift as users edit
- **Videos won't load** if files don't exist - users need to add their own media
- **Interpolation slider** will show "Loading..." if frames don't exist - this is expected for the template
- The template is based on Nerfies project page - footer attribution should remain per CC BY-SA 4.0 license
