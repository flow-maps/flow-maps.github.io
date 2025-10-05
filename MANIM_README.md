# Flow Maps Manim Animation

This manim script creates an educational video illustrating the Flow Maps via Self-Distillation method.

The animation is split into 7 independent parts that can be rendered separately and combined later.

## Installation

First, install manim and ffmpeg:

```bash
pip install manim
# On macOS:
brew install ffmpeg
# On Ubuntu/Debian:
sudo apt-get install ffmpeg
```

## Rendering Individual Parts

Each part can be rendered independently:

```bash
# Part 0: Introduction
manim -pqh manim_flow_maps.py Part0_Introduction

# Part 1: Flow Matching Introduction
manim -pqh manim_flow_maps.py Part1_FlowMatching

# Part 2: Flow Map Definition
manim -pqh manim_flow_maps.py Part2_FlowMapDefinition

# Part 3: Tangent Condition
manim -pqh manim_flow_maps.py Part3_TangentCondition

# Part 4: Eulerian Loss
manim -pqh manim_flow_maps.py Part4_EulerianLoss

# Part 5: Progressive Loss
manim -pqh manim_flow_maps.py Part5_ProgressiveLoss

# Part 6: Lagrangian Loss
manim -pqh manim_flow_maps.py Part6_LagrangianLoss
```

Quality flags:
- `-pql`: Low quality (480p15), fast preview
- `-pqm`: Medium quality (720p30)
- `-pqh`: High quality (1080p60), recommended
- `-pqk`: 4K quality (2160p60)

## Rendering All Parts at Once

Use the provided script:

```bash
# High quality (default)
./render_all.sh

# Low quality for testing
./render_all.sh l

# Medium quality
./render_all.sh m

# 4K quality
./render_all.sh k
```

## Combining Videos

After rendering all parts, combine them into a single video:

```bash
./combine_videos.sh
```

This will create `static/videos/flow_maps_method.mp4` ready for the website.

For different quality levels:
```bash
# Low quality (480p15)
./combine_videos.sh 480p15

# Medium quality (720p30)
./combine_videos.sh 720p30

# High quality (1080p60) - default
./combine_videos.sh 1080p60

# 4K (2160p60)
./combine_videos.sh 2160p60
```

## Video Structure

0. **Part0_Introduction** (~15s)
   - Paper title and authors
   - Sets context for the presentation

1. **Part1_FlowMatching** (~30s)
   - Gaussian → Gaussian mixture via ODE trajectories
   - Visualizes standard flow matching

2. **Part2_FlowMapDefinition** (~30s)
   - Shows flow map jumping along trajectories
   - Introduces parameterization X_{s,t}(x) = x + (t-s)v_{s,t}(x)

3. **Part3_TangentCondition** (~45s)
   - Visualizes infinitesimally close points
   - Shows slope → velocity field
   - Derives v_{t,t} = b_t

4. **Part4_EulerianLoss** (~30s)
   - Two starting points → same endpoint
   - Notes connection to consistency models

5. **Part5_ProgressiveLoss** (~30s)
   - Jump composition: s→u→t = s→t
   - Notes connection to shortcut models

6. **Part6_LagrangianLoss** (~30s)
   - Points separated at endpoint
   - Highlights: follows trajectories, no spatial derivatives

**Total duration: ~3-3.5 minutes**

## Workflow

Typical workflow for iterative development:

```bash
# 1. Render one part at low quality for testing
manim -pql manim_flow_maps.py Part1_FlowMatching

# 2. Once satisfied, render at high quality
manim -pqh manim_flow_maps.py Part1_FlowMatching

# 3. Repeat for all parts (or use render_all.sh)

# 4. Combine all parts
./combine_videos.sh

# 5. Video is ready at static/videos/flow_maps_method.mp4
```

## Customization

Each part is independent, so you can modify:
- **Colors**: Change BLUE, RED, YELLOW, etc. in the code
- **Timing**: Adjust `run_time` and `wait()` durations
- **Individual parts**: Edit specific scenes without affecting others
- **Font sizes**: Modify `font_size` parameters

## Output

Individual parts are saved to:
```
media/videos/manim_flow_maps/{quality}/Part{N}_{Name}.mp4
```

Combined video:
```
static/videos/flow_maps_method.mp4
```
