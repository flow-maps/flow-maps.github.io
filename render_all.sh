#!/bin/bash

# Render all parts of the Flow Maps animation
# Usage: ./render_all.sh [quality]
# quality: l (low), m (medium), h (high, default), k (4k)

QUALITY=${1:-h}

echo "Rendering all parts at quality: $QUALITY"
echo "=========================================="

manim -pq${QUALITY} manim_flow_maps.py Part0_Introduction
manim -pq${QUALITY} manim_flow_maps.py Part1_FlowMatching
manim -pq${QUALITY} manim_flow_maps.py Part2_FlowMapDefinition
manim -pq${QUALITY} manim_flow_maps.py Part3_TangentCondition
manim -pq${QUALITY} manim_flow_maps.py Part4_EulerianLoss
manim -pq${QUALITY} manim_flow_maps.py Part5_ProgressiveLoss
manim -pq${QUALITY} manim_flow_maps.py Part6_LagrangianLoss
manim -pq${QUALITY} manim_flow_maps.py Part7_MethodComparison

echo "=========================================="
echo "All parts rendered successfully!"
echo "Output directory: media/videos/manim_flow_maps/${QUALITY}/"
