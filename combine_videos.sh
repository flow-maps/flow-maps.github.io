#!/bin/bash

# Combine all rendered parts into a single video
# Requires ffmpeg

QUALITY=${1:-1080p60}

echo "Combining videos from quality: $QUALITY"
echo "=========================================="

INPUT_DIR="media/videos/manim_flow_maps/${QUALITY}"
OUTPUT_FILE="static/videos/flow_maps_method.mp4"

# Create a file list for ffmpeg
cat > /tmp/video_list.txt << EOF
file '${PWD}/${INPUT_DIR}/Part0_Introduction.mp4'
file '${PWD}/${INPUT_DIR}/Part1_FlowMatching.mp4'
file '${PWD}/${INPUT_DIR}/Part2_FlowMapDefinition.mp4'
file '${PWD}/${INPUT_DIR}/Part3_TangentCondition.mp4'
file '${PWD}/${INPUT_DIR}/Part4_EulerianLoss.mp4'
file '${PWD}/${INPUT_DIR}/Part5_ProgressiveLoss.mp4'
file '${PWD}/${INPUT_DIR}/Part6_LagrangianLoss.mp4'
file '${PWD}/${INPUT_DIR}/Part7_MethodComparison.mp4'
EOF

# Combine using ffmpeg
ffmpeg -f concat -safe 0 -i /tmp/video_list.txt -c copy ${OUTPUT_FILE}

echo "=========================================="
echo "Combined video saved to: ${OUTPUT_FILE}"
echo "Duration: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${OUTPUT_FILE}) seconds"

# Clean up
rm /tmp/video_list.txt
