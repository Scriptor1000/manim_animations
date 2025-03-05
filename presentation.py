import os

import numpy as np
from manim import *


def calculate_square(p1, p2):
    # Vektor der Linie zwischen den Punkten p1 und p2
    line_vector = p2 - p1

    # Normalisieren und skalieren
    rot_vector = [line_vector[1], -line_vector[0], 0]

    # Punkte des Quadrats berechnen
    p3 = p2 + rot_vector
    p4 = p1 + rot_vector

    return [p1, p4, p3, p2]


class Parallelogram(Scene):
    def construct(self):
        initial_points = [
            np.array([0, 0, 0]),  # A
            np.array([2, 0, 0]),  # B
            np.array([3, 2, 0]),  # C
            np.array([1, 2, 0]),  # D
        ]
        colors = [
            YELLOW,  # AB
            RED,  # BC
            GREEN,  # CD
            PURPLE,  # DA
        ]
        parallelogram = Polygon(
            *initial_points,  # Eckpunkte
            color=BLUE, fill_opacity=0.5
        ).center()

        self.play(Create(parallelogram))

        edge_polygons = []
        squares = []
        points = parallelogram.get_vertices()
        for i in range(4):
            edge_polygons.append(
                Polygon(points[i], points[i], points[(i + 1) % 4], points[(i + 1) % 4], color=colors[i],
                        fill_opacity=0.2))
            squares.append(
                Polygon(*calculate_square(points[i], points[(i + 1) % 4]), color=colors[i], fill_opacity=0.2))

        self.play(*[Create(edge_polygon) for edge_polygon in edge_polygons])
        self.play(*[Transform(edge_polygon, square) for edge_polygon, square in zip(edge_polygons, squares)])

        diagonals = [
            (
                Line(vertices[0], vertices[2], color=WHITE, fill_opacity=0.15),
                Line(vertices[3], vertices[1], color=WHITE, fill_opacity=0.15)
            )
            for vertices in map(lambda s: s.get_vertices(), squares)
        ]
        # all diagonals in a single dimension list
        all_diagonals = [diagonal[0] for diagonal in diagonals] + [diagonal[1] for diagonal in diagonals]
        centers = [s.get_center() for s in squares]
        center_dots = [Dot(center, color=WHITE) for center in centers]

        self.play(*[Create(diagonal) for diagonal in all_diagonals])
        self.play(*[Create(center_dot) for center_dot in center_dots])
        self.play(*[Uncreate(diagonal) for diagonal in all_diagonals])

        center_square = Polygon(*[center for center in centers], color=WHITE, fill_opacity=0)
        self.play(Create(center_square))

        edges = [Line(centers[i], centers[(i + 1) % 4]) for i in range(4)]
        angles = [
            RightAngle(edges[i], edges[(i + 1) % 4], length=0.2, quadrant=(-1, 1))
            for i in range(4)
        ]
        self.play(*[Create(angle) for angle in angles])


def align_to_tex_top(to_aligned: MathTex, top_aligned: MathTex) -> MathTex:
    return to_aligned.next_to(top_aligned, DOWN, buff=0.5).align_to(top_aligned, LEFT)


class RotateAroundPoint(Scene):
    def construct(self):
        plane = ComplexPlane(x_range=(-2, 5, 1), y_range=(-1, 6, 1)).add_coordinates().to_edge(LEFT)
        self.play(Create(plane))

        fixed = 3 + 1j
        rotating = 4 + 2j
        # Punkte
        fixed_point = Dot(plane.n2p(fixed), color=BLUE)
        fixed_point_label = MathTex("P", color=BLUE).next_to(fixed_point, (DOWN + RIGHT) / 2)
        rotating_origin_point = Dot(plane.n2p(rotating), color=RED)
        rotating_origin_point_label = MathTex("Q", color=RED).next_to(rotating_origin_point, (DOWN + RIGHT) / 2)

        self.play(Create(fixed_point), Create(rotating_origin_point))
        self.play(Write(fixed_point_label), Write(rotating_origin_point_label))

        fixed_point_label_extended = MathTex("P=3+i").next_to(plane, RIGHT, buff=1).align_to(plane, UP)
        rotating_origin_point_label_extended = align_to_tex_top(MathTex("Q=4+2i"), fixed_point_label_extended)
        self.play(Write(fixed_point_label_extended), Write(rotating_origin_point_label_extended))

        tight = Line(fixed_point.get_center(), rotating_origin_point.get_center(), color=GREEN)
        rotating_point = Dot(rotating_origin_point.get_center(), color=GREEN)
        angle_arc = Arc(
            radius=0.5,
            start_angle=tight.get_angle(),
            angle=PI / 2,
            arc_center=fixed_point.get_center(),
            color=YELLOW
        )
        self.play(Create(tight), Create(rotating_point))
        self.play(Rotate(rotating_point, angle=PI / 2, about_point=fixed_point.get_center(), ),
                  Rotate(tight, angle=PI / 2, about_point=fixed_point.get_center(), ),
                  Create(angle_arc, ))

        rotating_point_label = MathTex("Q'", color=GREEN).next_to(rotating_point, DOWN)
        label_rotated = align_to_tex_top(MathTex("Q'=2+2i"), rotating_origin_point_label_extended)
        self.play(Write(rotating_point_label), Write(label_rotated))
        self.play(FadeOut(rotating_point_label), FadeOut(label_rotated), FadeOut(angle_arc), FadeOut(tight),
                  FadeOut(rotating_point), )

        tight = Line(fixed_point.get_center(), rotating_origin_point.get_center(), color=GREEN)
        point_zero = plane.n2p(0)
        vector_fixed = Line(point_zero, fixed_point.get_center(), color=YELLOW)
        help_dot = Dot(plane.n2p(rotating - fixed), color=GREEN)
        help_label = MathTex("H", color=GREEN).next_to(help_dot, (UP + RIGHT) / 2, )
        help_label_extended = align_to_tex_top(MathTex("H=Q-P=1+i"),
                                               rotating_origin_point_label_extended)

        self.play(Create(tight), Create(vector_fixed))
        self.play(tight.animate.shift(point_zero - fixed_point.get_center()))
        self.play(Create(help_dot), Write(help_label), Write(help_label_extended))

        angle_arc = Arc(
            radius=0.5,
            start_angle=tight.get_angle(),
            angle=PI / 2,
            arc_center=point_zero,
            color=YELLOW
        )
        help_dot2 = Dot(plane.n2p((rotating - fixed) * 1j), color=GREEN)
        help_label2 = MathTex("H'", color=GREEN).next_to(help_dot2, (UP + LEFT) / 2, )
        help_label2_extended = align_to_tex_top(MathTex("H'=H\cdot i=-1+i"), help_label_extended)

        final_dot = Dot(plane.n2p((rotating - fixed) * 1j + fixed), color=GREEN)
        final_label = MathTex("Q'", color=GREEN).next_to(final_dot, (UP + RIGHT) / 2, )
        final_label_extended = align_to_tex_top(
            MathTex("Q'&=H'+P=H\cdot i +P\\\\&=(Q-P)\cdot i + P\\\\&=(1+i)\cdot i + 3 +i\\\\&=2+2i"),
            help_label2_extended)

        self.play(Create(angle_arc), Rotate(tight, angle=PI / 2, about_point=point_zero, ))
        self.play(Create(help_dot2), Write(help_label2), Write(help_label2_extended))

        self.play(vector_fixed.animate.shift(help_dot2.get_center() - point_zero), FadeOut(angle_arc), FadeOut(tight))
        self.play(Write(final_label), Create(final_dot), )
        self.play(Write(final_label_extended), FadeOut(vector_fixed))

        fixed = 1 + 2j
        new_fixed_position = plane.n2p(fixed)
        rotating = 4 + 3j
        new_rotating_position = plane.n2p(rotating)
        new_fixed_point_label_extended = MathTex("P=1+2i").move_to(fixed_point_label_extended)
        new_rotating_origin_point_label_extended = align_to_tex_top(MathTex("Q=4+3i"),
                                                                    new_fixed_point_label_extended)
        hint_label = align_to_tex_top(MathTex("Q'=(Q-P)\cdot i+P"), new_rotating_origin_point_label_extended)
        answer_tex = "Q'&=(3+i)\cdot i+P\\\\&=3i-1+1+2i\\\\&=0+5i"
        answer_label = align_to_tex_top(MathTex(answer_tex), hint_label)

        self.play(
            fixed_point.animate.move_to(new_fixed_position),
            rotating_origin_point.animate.move_to(new_rotating_position),
            fixed_point_label.animate.next_to(new_fixed_position, (DOWN + RIGHT) / 2),
            rotating_origin_point_label.animate.next_to(new_rotating_position, (DOWN + RIGHT) / 2),
            FadeOut(help_dot), FadeOut(help_label), FadeOut(help_label_extended),
            FadeOut(help_dot2), FadeOut(help_label2), FadeOut(help_label2_extended),
            FadeOut(final_dot), FadeOut(final_label), FadeOut(final_label_extended),
            Transform(fixed_point_label_extended, new_fixed_point_label_extended),
            Transform(rotating_origin_point_label_extended, new_rotating_origin_point_label_extended),
        )
        self.play(Write(hint_label))
        self.play(Write(answer_label))
        self.play(
            Uncreate(plane),
            Uncreate(fixed_point), Uncreate(rotating_origin_point),
            Uncreate(fixed_point_label), Uncreate(rotating_origin_point_label),
            Uncreate(fixed_point_label_extended), Uncreate(rotating_origin_point_label_extended),
            Uncreate(hint_label), Uncreate(answer_label),
        )


class SolveParallelogram(Scene):
    def construct(self):
        initial_points = [
            np.array([0, 0, 0]),  # A
            np.array([2, 0, 0]),  # B
            np.array([3, 2, 0]),  # C
            np.array([1, 2, 0]),  # D
        ]

        plane = ComplexPlane(x_range=(-1.5, 3, 1), y_range=(-1.5, 2.5, 1)).add_coordinates(
            -1, 2, 2j, -1j
        ).scale(1.5).to_edge(LEFT)
        plane_points = [plane.n2p(0),
                        plane.n2p(1),
                        plane.n2p(1.5 + 1j),
                        plane.n2p(.5 + 1j), ]

        centered_parallelogram = Polygon(
            *initial_points,  # Eckpunkte
            color=BLUE, fill_opacity=0.5
        ).center()
        plane_parallelogram = Polygon(
            *plane_points,  # Eckpunkte
            color=BLUE, fill_opacity=0.5
        )
        corner_names = ["A", "B", "C", "D"]
        point_labels = [MathTex(label).next_to(point, direction) for label, direction, point in
                        zip(corner_names,
                            [DOWN + LEFT / 2, DOWN + RIGHT / 2, UP + RIGHT / 2, UP + LEFT / 2],
                            plane_points)]

        self.play(Create(centered_parallelogram))
        self.play(Transform(centered_parallelogram, plane_parallelogram), Create(plane))
        self.play(*[Write(label) for label in point_labels])

        point_a_description = MathTex("A=0").next_to(plane, RIGHT, aligned_edge=UP, buff=0.75)
        point_b_description = MathTex("B=1").next_to(point_a_description, RIGHT, buff=0.5)
        point_c_description = MathTex("C=B+D").next_to(point_b_description, RIGHT, buff=0.5)

        self.play(Write(point_a_description), Write(point_b_description), Write(point_c_description))

        edge_polygons = []
        squares = []
        points = plane_parallelogram.get_vertices()
        for i in range(4):
            edge_polygons.append(
                Polygon(points[i], points[i], points[(i + 1) % 4], points[(i + 1) % 4], color=GREEN,
                        fill_opacity=0.2))
            squares.append(
                Polygon(*calculate_square(points[i], points[(i + 1) % 4]), color=GREEN, fill_opacity=0.2,
                        stroke_opacity=0.5))

        self.play(*[Create(edge_polygon) for edge_polygon in edge_polygons])
        self.play(*[Transform(edge_polygon, square) for edge_polygon, square in zip(edge_polygons, squares)])

        new_points_e = [square.get_vertices()[1] for square in squares]
        e_directions = [(DOWN + LEFT) / 2, (DOWN + RIGHT) / 2, (UP + RIGHT) / 2, UP / 2]
        e_labels = [MathTex(f"E_{{{i + 1}}}", color=GREEN).next_to(point, direction) for i, (point, direction) in
                    enumerate(zip(new_points_e, e_directions))]
        new_points_f = [square.get_vertices()[2] for square in squares]
        f_directions = [(DOWN + RIGHT) / 2, (DOWN + RIGHT) / 2, (UP + LEFT) / 2, LEFT / 2]
        f_labels = [MathTex(f"F_{{{i + 1}}}", color=GREEN).next_to(point, direction) for i, (point, direction) in
                    enumerate(zip(new_points_f, f_directions))]
        dots = [Dot(point, color=GREEN) for point in new_points_e + new_points_f]
        self.play(*[Write(label) for label in e_labels + f_labels],
                  *[Create(dot) for dot in dots])

        f_description_texs = [
            f"F_{{{i + 1}}}=({corner_names[i]} - {corner_names[(i + 1) % 4]})\cdot i + {corner_names[(i + 1) % 4]}"
            for i in range(4)]
        e_description_texs = [
            f"E_{{{i + 1}}}=({corner_names[i]} - {corner_names[(i + 1) % 4]})\cdot i + {corner_names[i]}"
            for i in range(4)
        ]
        f_description_labels = [MathTex(description_tex) for description_tex in f_description_texs]
        e_description_labels = [MathTex(description_tex) for description_tex in e_description_texs]
        align_to_tex_top(f_description_labels[0], point_a_description)
        align_to_tex_top(e_description_labels[0], f_description_labels[0])
        e_hint_descriptions = [
            align_to_tex_top(MathTex(tex_str), f_description_labels[0])
            for tex_str in ["E_1=(B-A)\cdot i^3+A", "E_1=-(B-A)\cdot i+A"]
        ]
        # for i in range(1, 3):
        #     align_to_tex_top(f_description_labels[i], e_description_labels[i - 1])
        #     align_to_tex_top(e_description_labels[i], f_description_labels[i])
        f_help_line = Line(plane_points[1], plane_points[0], color=YELLOW)
        self.play(Create(f_help_line))
        self.play(Rotate(f_help_line, angle=PI / 2, about_point=plane_points[1]))
        self.play(Write(f_description_labels[0]), Rotate(f_help_line, angle=-PI / 2, about_point=plane_points[1]))
        self.play(Rotate(f_help_line, angle=3 * PI / 2, about_point=plane_points[0]))
        self.play(Write(e_hint_descriptions[0]), Uncreate(f_help_line))
        self.play(Transform(e_hint_descriptions[0], e_hint_descriptions[1]))
        self.play(Transform(e_hint_descriptions[0], e_description_labels[0]))

        midpoints = [np.array(sum(squares[i].get_vertices()) / 4) for i in range(4)]
        mid_dot = [Dot(point, color=YELLOW) for point in midpoints]
        mid_directions = [DOWN / 2, RIGHT / 2, UP / 2, LEFT / 2]
        mid_labels = [MathTex(f"M_{{{i + 1}}}", color=YELLOW).next_to(point, direction) for i, (point, direction) in
                      enumerate(zip(midpoints, mid_directions))]
        center_square = Polygon(*midpoints, color=YELLOW, fill_opacity=00)
        # self.play(*[Write(label) for label in mid_labels],
        #           *[Create(dot) for dot in mid_dot])
        # self.play(Create(center_square))
        self.play(Write(mid_labels[0]), Create(mid_dot[0]))
        mid_label_description = align_to_tex_top(MathTex("M_1=\\frac{A+B+E_1+F_1}{4}"), e_description_labels[0])
        mid_label_descriptions = [
            MathTex(
                f"M_{{{i + 1}}}=\\frac{{{corner_names[i]}+{corner_names[(i + 1) % 4]}+"
                f"{corner_names[i]}i-{corner_names[(i + 1) % 4]}i}}{{2}}")
            for i in range(4)
        ]
        align_to_tex_top(mid_label_descriptions[0], e_description_labels[0])
        self.play(Write(mid_label_description))
        self.play(Transform(mid_label_description, mid_label_descriptions[0]))
        self.play(FadeOut(e_hint_descriptions[0]), FadeOut(f_description_labels[0]),
                  mid_label_description.animate.next_to(point_a_description, DOWN, buff=0.5).align_to(
                      point_a_description, LEFT))
        align_to_tex_top(mid_label_descriptions[1], mid_label_description)
        for i in range(2, 4):
            align_to_tex_top(mid_label_descriptions[i], mid_label_descriptions[i - 1])

        self.play(*[Create(dot) for dot in mid_dot[1:]],
                  *[Write(label) for label in mid_labels[1:]],
                  *[Write(description) for description in mid_label_descriptions[1:]])

        self.play(Create(center_square))

        help_line = Line(midpoints[0], midpoints[1], color=RED)
        self.play(Create(help_line))
        self.play(Rotate(help_line, angle=PI / 2, about_point=midpoints[0]))
