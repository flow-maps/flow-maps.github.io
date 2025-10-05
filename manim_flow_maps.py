"""
Manim animation for Flow Maps via Self-Distillation

Each part is a separate Scene that can be rendered independently:
0. Part0_Introduction - Title and authors
1. Part1_FlowMatching - Standard flow matching (Gaussian → Gaussian mixture)
2. Part2_FlowMapDefinition - Flow map definition (jumps along trajectories)
3. Part3_TangentCondition - Tangent condition (v_{t,t} = b_t)
4. Part4_EulerianLoss - Eulerian self-distillation
5. Part5_ProgressiveLoss - Progressive self-distillation
6. Part6_LagrangianLoss - Lagrangian self-distillation

Render each with:
    manim -pqh manim_flow_maps.py Part0_Introduction
"""

from manim import *
import numpy as np


# ============================================================================
# PART 1: Flow Matching Introduction
# ============================================================================

class Part1_FlowMatching(Scene):
    def construct(self):
        """Part 1: Illustrate standard flow matching with curved ODE trajectories"""

        # Section title
        section_title = Text("Flow Matching", font_size=36)
        section_subtitle = Text("with stochastic interpolants", font_size=24, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.2)
        title_group = VGroup(section_title, section_subtitle)
        title_group.to_edge(UP)
        self.play(Write(section_title), Write(section_subtitle))
        self.wait(0.5)

        # Create axes (invisible, just for coordinate system)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(UP * 0.5)

        # Time and distribution labels
        t0_label = MathTex("t=0", font_size=30).move_to(axes.c2p(-3.5, 2.5))
        t1_label = MathTex("t=1", font_size=30).move_to(axes.c2p(3.5, 2.5))
        rho0_label = MathTex(r"\rho_0", font_size=28).move_to(axes.c2p(-2.5, -1.2))
        rho1_label = MathTex(r"\rho_1", font_size=28).move_to(axes.c2p(2.0, -2.0))

        self.play(Write(t0_label), Write(t1_label))

        # Initial distribution (Gaussian centered at origin)
        def gaussian_sample(n_points, center, scale):
            return np.random.randn(n_points, 2) * scale + center

        # Create initial points (t=0)
        n_points = 150
        initial_points = gaussian_sample(n_points, np.array([-2.5, 0]), 0.3)
        dots_t0 = VGroup(*[
            Dot(axes.c2p(p[0], p[1]), radius=0.03, color="#C77DFF")  # Vibrant light purple
            for p in initial_points
        ])

        # Target distribution (two-mode Gaussian mixture at t=1)
        target_points = []
        for i, p in enumerate(initial_points):
            if i < n_points // 2:
                target = gaussian_sample(1, np.array([2.0, 1.2]), 0.25)[0]
            else:
                target = gaussian_sample(1, np.array([2.0, -1.2]), 0.25)[0]
            target_points.append(target)
        target_points = np.array(target_points)

        self.play(FadeIn(dots_t0), Write(rho0_label))
        self.wait(0.5)

        # Create target dots (keep initial cloud in place)
        dots_t1 = VGroup(*[
            Dot(axes.c2p(p[0], p[1]), radius=0.03, color="#C77DFF")
            for p in target_points
        ])
        dots_t1.set_z_index(1)

        # Show target distribution
        self.play(FadeIn(dots_t1), Write(rho1_label), run_time=1.5)
        self.wait(0.5)

        # Create curved ODE trajectories - 2 to each mode
        # Mode 1 (upper): two trajectories from upper half of Gaussian
        start1_upper = np.array([-2.5, 0.4])
        end1_upper = np.array([2.0, 1.5])
        start2_upper = np.array([-2.5, 0.2])
        end2_upper = np.array([2.0, 0.9])

        # Mode 2 (lower): two trajectories from lower half of Gaussian
        start1_lower = np.array([-2.5, -0.2])
        end1_lower = np.array([2.0, -0.9])
        start2_lower = np.array([-2.5, -0.4])
        end2_lower = np.array([2.0, -1.5])

        def curved_path(start, end, curve_amount=0.3):
            """Create a bezier-like curved path"""
            def path_func(t):
                # Cubic bezier with control points for curvature
                p0 = start
                p3 = end
                # Control points create the curve
                mid = (start + end) / 2
                p1 = start + (mid - start) * 0.5 + np.array([0, curve_amount])
                p2 = end + (mid - end) * 0.5 - np.array([0, curve_amount])

                # Cubic bezier formula
                point = (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
                return axes.c2p(point[0], point[1])
            return path_func

        # Create the 4 trajectories
        trajectories = VGroup()
        curves_params = [
            (start1_upper, end1_upper, 0.4),
            (start2_upper, end2_upper, 0.3),
            (start1_lower, end1_lower, -0.3),
            (start2_lower, end2_lower, -0.4),
        ]

        for start, end, curve in curves_params:
            path = ParametricFunction(
                curved_path(start, end, curve),
                t_range=[0, 1],
                color="#9D4EDD",  # Vibrant medium purple
                stroke_width=2.5
            )
            trajectories.add(path)

        # Set z-index so trajectories are in background, points in foreground
        trajectories.set_z_index(-1)
        dots_t0.set_z_index(1)

        # Animate all curved trajectories at once
        self.play(*[Create(traj) for traj in trajectories], run_time=2)
        self.wait(0.5)

        # Create moving points that travel along the trajectories
        moving_dots = VGroup(*[
            Dot(axes.c2p(start[0], start[1]), radius=0.04, color="#E0AAFF")
            for start, _, _ in curves_params
        ])
        moving_dots.set_z_index(2)  # Even more in foreground

        # Animate points moving along the 4 curved paths
        move_animations = []
        for i, (moving_dot, (start, end, curve)) in enumerate(zip(moving_dots, curves_params)):
            # Create path for MoveAlongPath
            path = ParametricFunction(
                curved_path(start, end, curve),
                t_range=[0, 1],
            )
            move_animations.append(MoveAlongPath(moving_dot, path))

        self.play(*[FadeIn(dot) for dot in moving_dots])
        self.play(*move_animations, run_time=2.5)
        self.wait(0.3)

        # Fade out moving dots
        self.play(FadeOut(moving_dots), run_time=0.5)
        self.wait(0.5)

        # Add probability flow ODE
        ode_eq = MathTex(
            r"\dot{x}_t = b_t(x_t), \quad x_0 \sim \rho_0",
            font_size=30
        ).to_edge(DOWN).shift(UP * 2.2)
        self.play(Write(ode_eq))
        self.wait(0.5)

        # Add conditional expectation and loss
        cond_exp = MathTex(
            r"b_t(x) = \mathbb{E}[\dot{I}_t \mid I_t = x]",
            font_size=28
        ).to_edge(DOWN).shift(UP * 1.6)
        self.play(Write(cond_exp))
        self.wait(0.5)

        loss_eq = MathTex(
            r"\mathcal{L}(\hat{b}) = \mathbb{E}\left[|\hat{b}_t(I_t) - \dot{I}_t|^2\right]",
            font_size=28
        ).to_edge(DOWN).shift(UP * 0.9)
        self.play(Write(loss_eq))
        self.wait(0.5)

        # Add note about expensive ODE solve
        note_text = Text(
            "highly expressive model class, but requires an expensive differential equation solve for inference!",
            font_size=22,
            color=WHITE
        ).to_edge(DOWN).shift(UP * 0.2)
        self.play(Write(note_text))
        self.wait(1.5)


# ============================================================================
# PART 2: Flow Map Definition
# ============================================================================

class Part2_FlowMapDefinition(Scene):
    def construct(self):
        """Part 2: Define the flow map as jumps along trajectories"""

        # Title and subtitle
        section_title = Text("The Flow Map", font_size=36)
        section_subtitle = Text("jumping along trajectories", font_size=24, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.2)
        title_group = VGroup(section_title, section_subtitle)
        title_group.to_edge(UP)
        self.play(Write(section_title), Write(section_subtitle))

        # Create a smooth trajectory through 2D space (no axes needed)
        def trajectory(t):
            # Smooth S-curve with gentle variation
            x = -3 + 6 * t
            y = 1.5 * np.sin(1.8 * PI * t) * (1 - 0.5 * t) + 0.4 * t * (1 - t) * np.sin(4 * PI * t)
            return np.array([x, y, 0])

        path = ParametricFunction(
            lambda t: trajectory(t),
            t_range=[0, 1],
            color="#9D4EDD",  # Medium purple
            stroke_width=3
        ).shift(UP * 0.8)

        self.play(Create(path), run_time=1.5)
        self.wait(0.5)

        # Show jumping from s to t
        s_val = 0.25
        t_val = 0.75

        x_s = Dot(trajectory(s_val) + UP * 0.8, color="#C77DFF", radius=0.08)  # Light purple
        x_t = Dot(trajectory(t_val) + UP * 0.8, color="#E0AAFF", radius=0.08)  # Lighter purple

        s_label = MathTex("x_s", font_size=28).next_to(x_s, DOWN, buff=0.2)
        t_label = MathTex("x_t", font_size=28).next_to(x_t, DOWN, buff=0.2)

        self.play(FadeIn(x_s), Write(s_label))
        self.wait(0.3)

        # Show the jump (curved arrow for better spacing)
        arrow = CurvedArrow(
            x_s.get_center(),
            x_t.get_center(),
            color="#7B2CBF",  # Darker purple
            angle=-TAU/8,
            stroke_width=6,
            tip_length=0.2
        )

        self.play(Create(arrow))
        self.play(FadeIn(x_t), Write(t_label))
        self.wait(0.5)

        # Write flow map definition
        flow_map_def = MathTex(
            r"X_{s,t}(x_s) = x_t",
            font_size=36
        ).to_edge(DOWN).shift(UP * 2.4)

        self.play(Write(flow_map_def))
        self.wait(1)

        # Explain advantage: no ODE solving
        advantage_text = MathTex(
            r"X_{s,t} \text{ enables fast inference by avoiding a differential equation solve}",
            font_size=26,
            color=WHITE
        ).next_to(flow_map_def, DOWN, buff=0.4)

        self.play(Write(advantage_text))
        self.wait(1.5)

        # Raise the key question
        question_text = Text(
            "But how do we learn it?",
            font_size=28,
            color=WHITE,
            slant=ITALIC
        ).next_to(advantage_text, DOWN, buff=0.4)

        self.play(Write(question_text))
        self.wait(1)

        # Show the proposed parameterization
        parameterization = MathTex(
            r"\text{we propose the parameterization } \hat{X}_{s,t}(x) = x + (t-s)\hat{v}_{s,t}(x)",
            font_size=26,
            color=WHITE
        ).next_to(question_text, DOWN, buff=0.4)

        self.play(Write(parameterization))
        self.wait(2)


# ============================================================================
# PART 3: Tangent Condition
# ============================================================================

class Part3_TangentCondition(Scene):
    def construct(self):
        """Part 3: Illustrate the tangent condition"""

        # Title and subtitle
        section_title = Text("The Tangent Condition", font_size=36)
        section_subtitle = Text("connecting flow maps to flows", font_size=24, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.2)
        title_group = VGroup(section_title, section_subtitle)
        title_group.to_edge(UP)
        self.play(Write(section_title), Write(section_subtitle))

        # Use same trajectory as Part2 (smooth S-curve, no axes)
        def trajectory(t):
            # Smooth S-curve with gentle variation
            x = -3 + 6 * t
            y = 1.5 * np.sin(1.8 * PI * t) * (1 - 0.5 * t) + 0.4 * t * (1 - t) * np.sin(4 * PI * t)
            return np.array([x, y, 0])

        path = ParametricFunction(
            lambda t: trajectory(t),
            t_range=[0, 1],
            color="#9D4EDD",  # Medium purple
            stroke_width=3
        ).shift(UP * 0.5)

        self.play(Create(path), run_time=1.5)
        self.wait(0.5)

        # Show two infinitesimally close points (pick curved region near extremum)
        t_val = 0.3  # Near maximum - high curvature
        delta = 0.15

        # x_s starts away from x_t, will move toward it
        x_s = Dot(trajectory(t_val - delta) + UP * 0.5, color="#C77DFF", radius=0.08)  # Light purple
        x_t = Dot(trajectory(t_val) + UP * 0.5, color="#E0AAFF", radius=0.08)  # Lighter purple (stays fixed)

        s_label = MathTex("x_s", font_size=28).next_to(x_s, DOWN, buff=0.2)
        t_label = MathTex("x_t", font_size=28).next_to(x_t, UP, buff=0.2)

        self.play(FadeIn(x_s), FadeIn(x_t), Write(s_label), Write(t_label))

        # Draw line between them (secant)
        secant = Line(x_s.get_center(), x_t.get_center(), color="#7B2CBF", stroke_width=3)  # Darker purple
        self.play(Create(secant))
        self.wait(0.5)

        # Show slope label (positioned lower to avoid overlap)
        slope_label = MathTex(
            r"\text{slope}_{s,t} = \frac{x_t - x_s}{t - s} = \frac{X_{s,t}(x_s) - x_s}{t - s}",
            font_size=26
        ).to_edge(DOWN).shift(UP * 1.5)
        self.play(Write(slope_label))
        self.wait(0.5)

        # Shrink delta (x_s approaches x_t)
        for new_delta in [0.1, 0.05, 0.02]:
            new_x_s = Dot(trajectory(t_val - new_delta) + UP * 0.5, color="#C77DFF", radius=0.08)  # Light purple
            new_s_label = MathTex("x_s", font_size=28).next_to(new_x_s, DOWN, buff=0.2)
            new_secant = Line(new_x_s.get_center(), x_t.get_center(), color="#7B2CBF", stroke_width=3)  # Darker purple

            self.play(
                Transform(x_s, new_x_s),
                Transform(s_label, new_s_label),
                Transform(secant, new_secant),
                run_time=0.8
            )
            self.wait(0.3)

        # Extend tangent line (arrow) when points are close
        tangent_direction = trajectory(t_val + 0.001) - trajectory(t_val - 0.001)
        tangent_direction = tangent_direction / np.linalg.norm(tangent_direction)
        tangent_arrow = Arrow(
            x_t.get_center() - tangent_direction * 1.2,
            x_t.get_center() + tangent_direction * 1.2,
            color="#E0AAFF",  # Lightest purple
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.1
        )

        # Label tangent arrow (positioned to avoid graph)
        tangent_label = MathTex("b_t(x) = v_{t,t}(x)", font_size=28, color="#E0AAFF").move_to(
            x_t.get_center() + tangent_direction * 2.5 + UP * 0.5
        )

        self.play(Create(tangent_arrow), Write(tangent_label))
        self.wait(1)

        # Show tangent condition
        tangent_eq = MathTex(
            r"\lim_{s \to t} \text{slope}_{s,t} = \lim_{s \to t} \partial_t X_{s,t}(x_t) = b_t(x_t) = v_{t,t}(x_t)",
            font_size=28
        ).next_to(slope_label, DOWN, buff=0.4)
        self.play(Write(tangent_eq))
        self.wait(1)

        # Add note about training like a flow
        flow_note = MathTex(
            r"\text{can train } v_{t,t} \text{ like a flow!}",
            font_size=26,
            color=WHITE
        ).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(flow_note))
        self.wait(1.5)


# ============================================================================
# PART 4: Eulerian Loss
# ============================================================================

class Part4_EulerianLoss(Scene):
    def construct(self):
        """Part 4a: Eulerian Self-Distillation"""

        # Title and subtitle
        section_title = Text("Eulerian Self-Distillation", font_size=36)
        section_subtitle = Text("recovers consistency distillation & training, align your flow, and mean flow", font_size=22, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.2)
        title_group = VGroup(section_title, section_subtitle)
        title_group.to_edge(UP)
        self.play(Write(section_title), Write(section_subtitle))
        self.wait(0.5)

        # Text explanation
        explanation = Text(
            "impose that infinitesimally-close starting points end at the same location",
            font_size=24,
            color=WHITE
        ).shift(UP * 2.0)
        self.play(Write(explanation))
        self.wait(0.5)

        # Condition equation
        condition = MathTex(
            r"X_{s,t}(x_s) = X_{s+\Delta s,t}(x_{s+\Delta s})",
            font_size=28
        ).next_to(explanation, DOWN, buff=0.3)
        self.play(Write(condition))
        self.wait(1)

        # Use same trajectory as Parts 2 & 3 (smooth S-curve, no axes)
        def trajectory(t):
            # Smooth S-curve with gentle variation
            x = -3 + 6 * t
            y = 1.5 * np.sin(1.8 * PI * t) * (1 - 0.5 * t) + 0.4 * t * (1 - t) * np.sin(4 * PI * t)
            return np.array([x, y, 0])

        path = ParametricFunction(
            lambda t: trajectory(t),
            t_range=[0, 1],
            color="#9D4EDD",  # Medium purple
            stroke_width=3
        ).shift(DOWN * 0.6)

        self.play(Create(path), run_time=1.5)
        self.wait(0.5)

        # Two starting points (infinitesimally close, near max for visual interest)
        s_val = 0.28  # Near maximum
        delta_s = 0.08
        t_val = 0.7

        x_s = Dot(trajectory(s_val) + DOWN * 0.6, color="#C77DFF", radius=0.08)  # Light purple
        x_s_delta = Dot(trajectory(s_val + delta_s) + DOWN * 0.6, color="#C77DFF", radius=0.08)  # Light purple
        x_t = Dot(trajectory(t_val) + DOWN * 0.6, color="#E0AAFF", radius=0.08)  # Lighter purple

        s_label = MathTex("x_s", font_size=24).next_to(x_s, DOWN, buff=0.15)
        s_delta_label = MathTex("x_{s+\Delta s}", font_size=24).next_to(x_s_delta, UP, buff=0.15)
        t_label = MathTex("x_t", font_size=24).next_to(x_t, DOWN, buff=0.15)

        self.play(
            FadeIn(x_s), FadeIn(x_s_delta), FadeIn(x_t),
            Write(s_label), Write(s_delta_label), Write(t_label)
        )

        # Show both mapping to same endpoint (curved arrows for better spacing)
        arrow1 = CurvedArrow(x_s.get_center(), x_t.get_center(), color="#E0AAFF", angle=-TAU/10, stroke_width=4, tip_length=0.2)  # Lightest purple
        arrow2 = CurvedArrow(x_s_delta.get_center(), x_t.get_center(), color="#E0AAFF", angle=TAU/10, stroke_width=4, tip_length=0.2)  # Lightest purple

        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # Add clarifying text
        limit_text = Text(
            "in the limit, this recovers the loss",
            font_size=24,
            color=WHITE
        ).to_edge(DOWN).shift(UP * 1.2)
        self.play(Write(limit_text))
        self.wait(0.5)

        # Show objective at bottom
        objective = MathTex(
            r"\mathcal{L}_{\text{ESD}}(\hat{v}) = \mathbb{E}\left[\left|\partial_s \hat{X}_{s,t}(I_t) + \nabla \hat{X}_{s,t}(I_t) \hat{v}_{t,t}(I_t)\right|^2 + \left|\hat{v}_{t,t}(I_t) - \dot{I}_t\right|^2\right]",
            font_size=24
        ).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(objective))
        self.wait(1.5)


# ============================================================================
# PART 5: Progressive Loss
# ============================================================================

class Part5_ProgressiveLoss(Scene):
    def construct(self):
        """Part 5: Progressive Self-Distillation"""

        # Title and subtitle
        section_title = Text("Progressive Self-Distillation", font_size=36)
        section_subtitle = Text("recovers shortcut models when discretized", font_size=24, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.2)
        title_group = VGroup(section_title, section_subtitle)
        title_group.to_edge(UP)
        self.play(Write(section_title), Write(section_subtitle))
        self.wait(0.5)

        # Text explanation
        explanation = Text(
            "impose that two jumps are equivalent to one larger jump",
            font_size=24,
            color=WHITE
        ).shift(UP * 2.0)
        self.play(Write(explanation))
        self.wait(0.5)

        # Condition equation
        condition = MathTex(
            r"X_{s,t}(x_s) = X_{u,t}(X_{s,u}(x_s))",
            font_size=28
        ).next_to(explanation, DOWN, buff=0.3)
        self.play(Write(condition))
        self.wait(1)

        # Use same trajectory as Parts 2 & 3 (smooth S-curve, no axes)
        def trajectory(t):
            # Smooth S-curve with gentle variation
            x = -3 + 6 * t
            y = 1.5 * np.sin(1.8 * PI * t) * (1 - 0.5 * t) + 0.4 * t * (1 - t) * np.sin(4 * PI * t)
            return np.array([x, y, 0])

        path = ParametricFunction(
            lambda t: trajectory(t),
            t_range=[0, 1],
            color="#9D4EDD",  # Medium purple
            stroke_width=3
        ).shift(DOWN * 0.6)

        self.play(Create(path), run_time=1.5)
        self.wait(0.5)

        # Three points: s, u, t
        s_val = 0.15
        u_val = 0.5
        t_val = 0.9

        x_s = Dot(trajectory(s_val) + DOWN * 0.6, color="#C77DFF", radius=0.08)  # Light purple
        x_u = Dot(trajectory(u_val) + DOWN * 0.6, color="#B794F6", radius=0.08)  # Mid-light purple
        x_t = Dot(trajectory(t_val) + DOWN * 0.6, color="#E0AAFF", radius=0.08)  # Lighter purple

        s_label = MathTex("x_s", font_size=24).next_to(x_s, DOWN, buff=0.15)
        u_label = MathTex("x_u", font_size=24).next_to(x_u, DOWN, buff=0.35)
        t_label = MathTex("x_t", font_size=24).next_to(x_t, DOWN, buff=0.15)

        self.play(
            FadeIn(x_s), FadeIn(x_u), FadeIn(x_t),
            Write(s_label), Write(u_label), Write(t_label)
        )

        # Show composition: s→u→t (curved arrows for better spacing)
        arrow1 = CurvedArrow(x_s.get_center(), x_u.get_center(), color="#E0AAFF", angle=TAU/12, stroke_width=4, tip_length=0.2)  # Lightest purple
        arrow2 = CurvedArrow(x_u.get_center(), x_t.get_center(), color="#E0AAFF", angle=TAU/12, stroke_width=4, tip_length=0.2)  # Lightest purple

        self.play(Create(arrow1))
        self.wait(0.3)
        self.play(Create(arrow2))
        self.wait(0.5)

        # Show direct jump s→t (curved for better spacing)
        arrow_direct = CurvedArrow(x_s.get_center(), x_t.get_center(), color="#5A189A", angle=-TAU/6, stroke_width=6, tip_length=0.25)  # Darkest purple for emphasis
        self.play(Create(arrow_direct))
        self.wait(1)

        # Add clarifying text
        limit_text = Text(
            "this leads to the loss",
            font_size=24,
            color=WHITE
        ).to_edge(DOWN).shift(UP * 1.2)
        self.play(Write(limit_text))
        self.wait(0.5)

        # Show objective at bottom
        objective = MathTex(
            r"\mathcal{L}_{\text{PSD}}(\hat{v}) = \mathbb{E}\left[\left|\hat{X}_{s,t}(I_t) - \hat{X}_{u,t}(\hat{X}_{s,u}(I_t))\right|^2 + \left|\hat{v}_{t,t}(I_t) - \dot{I}_t\right|^2\right]",
            font_size=24
        ).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(objective))
        self.wait(1.5)


# ============================================================================
# PART 6: Lagrangian Loss
# ============================================================================

class Part6_LagrangianLoss(Scene):
    def construct(self):
        """Part 6: Lagrangian Self-Distillation"""

        # Title and subtitle
        section_title = Text("Lagrangian Self-Distillation", font_size=36)
        section_subtitle = Text("a new way to train flow maps", font_size=24, color=GRAY)
        section_subtitle.next_to(section_title, DOWN, buff=0.2)
        title_group = VGroup(section_title, section_subtitle)
        title_group.to_edge(UP)
        self.play(Write(section_title), Write(section_subtitle))
        self.wait(0.5)

        # Text explanation
        explanation = Text(
            "impose consistency along trajectories by composing an infinitesimal jump",
            font_size=24,
            color=WHITE
        ).shift(UP * 2.0)
        self.play(Write(explanation))
        self.wait(0.5)

        # Condition equation
        condition = MathTex(
            r"X_{s,t}(x_s) = X_{t-\Delta t,t}(X_{s,t-\Delta t}(x_s))",
            font_size=26
        ).next_to(explanation, DOWN, buff=0.3)
        self.play(Write(condition))
        self.wait(1)

        # Use same trajectory as Parts 2 & 3 (smooth S-curve, no axes)
        def trajectory(t):
            # Smooth S-curve with gentle variation
            x = -3 + 6 * t
            y = 1.5 * np.sin(1.8 * PI * t) * (1 - 0.5 * t) + 0.4 * t * (1 - t) * np.sin(4 * PI * t)
            return np.array([x, y, 0])

        path = ParametricFunction(
            lambda t: trajectory(t),
            t_range=[0, 1],
            color="#9D4EDD",  # Medium purple
            stroke_width=3
        ).shift(DOWN * 0.6)

        self.play(Create(path), run_time=1.5)
        self.wait(0.5)

        # Points infinitesimally separated at endpoint (near minimum for spacing)
        s_val = 0.3
        t_val = 0.85  # Closer to minimum
        delta_t = 0.08

        x_s = Dot(trajectory(s_val) + DOWN * 0.6, color="#C77DFF", radius=0.08)  # Light purple
        x_t_delta = Dot(trajectory(t_val - delta_t) + DOWN * 0.6, color="#E0AAFF", radius=0.08)  # Lighter purple
        x_t = Dot(trajectory(t_val) + DOWN * 0.6, color="#E0AAFF", radius=0.08)  # Lighter purple

        s_label = MathTex("x_s", font_size=24).next_to(x_s, DOWN, buff=0.15)
        t_delta_label = MathTex("x_{t-\Delta t}", font_size=24).next_to(x_t_delta, DOWN, buff=0.15).shift(LEFT * 0.3)
        t_label = MathTex("x_t", font_size=24).next_to(x_t, DOWN, buff=0.15)

        self.play(
            FadeIn(x_s), FadeIn(x_t_delta), FadeIn(x_t),
            Write(s_label), Write(t_delta_label), Write(t_label)
        )

        # Show jumps (curved arrows for better spacing)
        arrow1 = CurvedArrow(x_s.get_center(), x_t_delta.get_center(), color="#E0AAFF", angle=TAU/12, stroke_width=4, tip_length=0.2)  # Lightest purple
        arrow_composition = CurvedArrow(x_t_delta.get_center(), x_t.get_center(), color="#E0AAFF", angle=TAU/12, stroke_width=4, tip_length=0.2)  # Composition arrow
        arrow2 = CurvedArrow(x_s.get_center(), x_t.get_center(), color="#E0AAFF", angle=-TAU/8, stroke_width=4, tip_length=0.2)  # Lightest purple

        self.play(Create(arrow1))
        self.wait(0.5)
        self.play(Create(arrow_composition))
        self.wait(0.5)
        self.play(Create(arrow2))
        self.wait(1)

        # Add clarifying text
        limit_text = Text(
            "in the limit, this recovers the loss",
            font_size=24,
            color=WHITE
        ).to_edge(DOWN).shift(UP * 1.2)
        self.play(Write(limit_text))
        self.wait(0.5)

        # Show objective at bottom
        objective = MathTex(
            r"\mathcal{L}_{\text{LSD}}(\hat{v}) = \mathbb{E}\left[\left|\partial_t \hat{X}_{s,t}(I_t) - \hat{v}_{t,t}(\hat{X}_{s,t}(I_t))\right|^2 + \left|\hat{v}_{t,t}(I_t) - \dot{I}_t\right|^2\right]",
            font_size=24
        ).to_edge(DOWN).shift(UP * 0.3)
        self.play(Write(objective))
        self.wait(1.5)


# ============================================================================
# PART 0: Introduction
# ============================================================================

class Part0_Introduction(Scene):
    def construct(self):
        """Introduction slide"""

        title = Text(
            "How to build a consistency model:\nLearning flow maps via self-distillation",
            font_size=40,
            line_spacing=1.2
        )
        title.move_to(UP * 1.5)

        authors = VGroup(
            Text("Nicholas M. Boffi (CMU)", font_size=26),
            Text("Michael Albergo (Harvard)", font_size=26),
            Text("Eric Vanden-Eijnden (Courant)", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.8)

        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(Write(authors), run_time=1.5)
        self.wait(2)
