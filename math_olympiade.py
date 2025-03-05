from manim import *


# manim .\math_olympiade.py Task641031 -ql

class Task641031(Scene):
    def construct(self):
        width = config.frame_width

        task_number = Tex('641031').scale(2).center()
        task_underline = Underline(task_number)
        self.play(Create(task_underline), Write(task_number))
        self.play(task_number.animate.to_edge(UP, buff=-2),
                  task_underline.animate.to_edge(UP, buff=-0.5), )

        eq1 = MathTex("99a+199b+299c+399d=3289", ).scale(1.5).center()
        eq2 = MathTex(r"99a+(100+99)b+(200+99)c+(300+99)d&=3289\\",
                      r"99a+99b+99c+99d+100b+200c+300d&=3289\\",
                      r"99(a+b+c+d)+100(b+2c+3d)&=3289", )
        self.play(Write(eq1))
        self.play(eq1.animate.to_edge(UP))
        for i in range(3):
            self.play(Write(eq2[i]))
        self.play(FadeOut(eq2[0]), FadeOut(eq2[1]), eq2[2].animate.next_to(eq1, DOWN))

        eq3 = MathTex(r"99(a+b+c+d) &\equiv 89 &&\pmod{100}\\",
                      r"-1(a+b+c+d) &\equiv -11 &&\pmod{100}\\",
                      r"a+b+c+d &\equiv 11 &&\pmod{100}\\", )
        for i in range(3):
            self.play(Write(eq3[i]))
        self.play(FadeOut(eq3[0]), FadeOut(eq3[1]), eq3[2].animate.next_to(eq2[2], DOWN))

        pos_1_4 = np.array([-width / 4, -1, 0])
        pos_3_4 = np.array([width / 4, -1, 0])
        eq4 = MathTex(r"a+b+c+d &= 11\\", r"99\cdot 11 &= 1089\\", r"100(b+2c+3d)&=2200\\")
        eq4 = eq4.move_to(pos_1_4)
        eq5 = MathTex(r"a+b+c+d &= 111\\", r"99\cdot 111 &= 10989\\ ", r"100(b+2c+3d)&=-7700\\", )
        eq5 = eq5.move_to(pos_3_4)
        for i in range(3):
            self.play(Write(eq4[i]), Write(eq5[i]))

        eq6 = MathTex(r"100(b+2c+3d)&=2200\\", r"b+2c+3d&=22").shift(DOWN)

        self.play(FadeOut(eq3[2]), FadeOut(eq5), FadeOut(eq4[1]),
                  eq4[0].animate.next_to(eq2[2], DOWN), Transform(eq4[2], eq6[0]))
        # eq4[3].next_to(eq4[2], DOWN)
        self.play(Write(eq6[1]))

        self.play(FadeOut(eq2[2]), eq4[0].animate.next_to(eq1, DOWN), eq6[1].animate.next_to(eq2[2], DOWN),
                  FadeOut(eq4[2]))

        eq7 = MathTex(r"b+2c+3d &= 2a+2b+2c+2d\\", "d &= 2a+b").shift(LEFT + DOWN)
        change7 = MathTex(r"|-b-2c-2d").to_edge(RIGHT).align_to(eq7[0], UP)
        self.play(Write(eq7[0]))
        self.play(Write(change7))
        self.play(Write(eq7[1]))

        self.play(FadeOut(eq7[0]), FadeOut(change7), eq7[1].animate.next_to(eq6[1], DOWN))

        eq8 = MathTex(r"3a+2b+c=11").next_to(eq7[1], DOWN)
        self.play(Write(eq8))

        equations = Group(eq8, eq7[1], eq6[1], eq4[0])
        self.play(equations.animate.scale(1.5).center().shift(DOWN / 2))

        # self.play(equations.animate.scale(2 / 3).next_to(eq1, DOWN))

        solution = MathTex(r"L=\{&(1,1,6,3), (1,2,4,4), (1,3,2,5),\\ &(2,1,3,5), (2,2,1,6)\}")
        solution.center().shift(DOWN / 2).scale(1.7)
        self.play(Transform(equations, solution))

        self.play(
            *[obj.animate.shift(LEFT * config.frame_width) for obj in self.mobjects],
            run_time=2
        )


def get_perpendicular(line, point):
    # Berechnung des Lotfußpunkts (senkrechter Projektion des Punktes auf die Linie)
    A, B = line.get_start(), line.get_end()
    P = point.get_center()

    # Richtungsvektor der Linie
    AB = B - A
    AB_unit = AB / np.linalg.norm(AB)  # Einheitsvektor

    # Projektion des Vektors AP auf AB (Skalarprojektion)
    AP = P - A
    projection_length = np.dot(AP, AB_unit)
    foot = A + projection_length * AB_unit  # Lotfußpunkt

    # Höhengerade von P zum Lotfußpunkt
    return Line(P, foot, color=GREEN)


def align_to_tex_top(to_aligned: MathTex, top_aligned: MathTex) -> MathTex:
    return to_aligned.next_to(top_aligned, DOWN, buff=0.5).align_to(top_aligned, LEFT)


class Task641032(Scene):
    def construct(self):
        width = config.frame_width
        height = config.frame_height

        task_number = Tex('641032').scale(2).center()
        task_underline = Underline(task_number)
        self.play(Create(task_underline), Write(task_number))
        self.play(task_number.animate.to_edge(UP, buff=-2),
                  task_underline.animate.to_edge(UP, buff=-0.5), )

        plane = NumberPlane(
            x_range=(-3.5, 3.5, 1),
            y_range=(-7.5, 4.5, 1),
        ).add_coordinates().scale_to_fit_height(height - 1).center().to_edge(LEFT)
        self.play(Create(plane))

        points = [
            plane.c2p(-1, -7),
            plane.c2p(3, 1),
            plane.c2p(-3, 4),
            plane.c2p(0, 0)
        ]
        dots = [Dot(p) for p in points]
        labels = [
            Text('A', font_size=24).next_to(dots[0], (DOWN + LEFT) / 2),
            Text('B', font_size=24).next_to(dots[1], (UP + RIGHT) / 2),
            Text('C', font_size=24).next_to(dots[2], (UP + RIGHT) / 2),
            Text('P', font_size=24).next_to(dots[3], (DOWN + RIGHT) / 2)
        ]
        for i in range(4):
            self.play(Create(dots[i]), Write(labels[i]))
        triangles = [
            Polygon(points[i], points[(i + 1) % 3], points[3], fill_color=BLUE, fill_opacity=0.2)
            for i in range(3)
        ]
        self.play(*[Create(t) for t in triangles])

        rects = [
            Polygon(plane.c2p(-1, -7), plane.c2p(3, -7), plane.c2p(3, 1), plane.c2p(-1, 1), color=YELLOW),
            Polygon(plane.c2p(-3, 0), plane.c2p(3, 0), plane.c2p(3, 4), plane.c2p(-3, 4), color=YELLOW),
            Polygon(plane.c2p(-3, -7), plane.c2p(0, -7), plane.c2p(0, 4), plane.c2p(-3, 4), color=YELLOW)
        ]
        # ABP
        self.play(triangles[0].animate.set_fill(opacity=0.5),
                  *[triangles[i].animate.set_stroke(opacity=0.2).set_fill(opacity=0) for i in range(1, 3)],
                  dots[2].animate.set_opacity(0.2), labels[2].animate.set_opacity(0.2))
        self.play(Create(rects[0]))
        help_points = [plane.c2p(0, 1), plane.c2p(-1, 0)]
        help_lines = [Line(p, points[3], color=RED) for p in help_points]
        self.play(*[Create(l) for l in help_lines])

        area_abp = MathTex(r"A_{ABP}&=32-16-\frac{3}{2}-\frac{7}{2}-1\\&=", '10')
        area_abp.next_to(plane, RIGHT, buff=1).align_to(plane, UP)
        self.play(Write(area_abp[0]))
        self.play(Write(area_abp[1]))

        # BCP
        self.play(triangles[1].animate.set_fill(opacity=0.5),
                  triangles[0].animate.set_stroke(opacity=0.2).set_fill(opacity=0),
                  dots[2].animate.set_opacity(1), labels[2].animate.set_opacity(1),
                  dots[0].animate.set_opacity(0.2), labels[0].animate.set_opacity(0.2),
                  ReplacementTransform(rects[0], rects[1]), *[Uncreate(l) for l in help_lines])

        area_bcp = MathTex(r"A_{BCP}&=24-\frac{3}{2}-9-6\\&=", r'\frac{15}{2}')
        align_to_tex_top(area_bcp, area_abp)
        self.play(Write(area_bcp[0]))
        self.play(Write(area_bcp[1]))

        # APC
        self.play(triangles[2].animate.set_fill(opacity=0.5),
                  triangles[1].animate.set_stroke(opacity=0.2).set_fill(opacity=0),
                  dots[0].animate.set_opacity(1), labels[0].animate.set_opacity(1),
                  dots[1].animate.set_opacity(0.2), labels[1].animate.set_opacity(0.2),
                  ReplacementTransform(rects[1], rects[2]))

        area_apc = MathTex(r"A_{APC}&=33-\frac{7}{2}-6-11\\&=", r'\frac{25}{2}')
        align_to_tex_top(area_apc, area_bcp)
        self.play(Write(area_apc[0]))
        self.play(Write(area_apc[1]))

        self.play(triangles[2].animate.set_stroke(opacity=0.2).set_fill(opacity=0),
                  dots[1].animate.set_opacity(1), labels[1].animate.set_opacity(1),
                  Uncreate(rects[2]), FadeOut(area_apc), FadeOut(area_bcp), FadeOut(area_abp))

        line_ac = Line(points[0], points[2], color=RED)
        perpendicular = get_perpendicular(line_ac, dots[3])
        self.play(Create(line_ac), dots[3].animate.set_color(RED), labels[3].animate.set_color(RED))
        self.play(Create(perpendicular))

        altitude = MathTex(r'A_{APC}&=\frac{1}{2}\cdot g \cdot h_g = \frac{25}{2}\\',
                           r"g&=\overline{AC}=\sqrt{2^2+11^2}=5\sqrt{5}\\",
                           r'h&=\frac{2\cdot A_{APC}}{g}=\frac{25}{5\sqrt{5}}\\',
                           r'&=\frac{5}{\sqrt{5}}=\sqrt{5}')
        altitude.next_to(plane, RIGHT, buff=1).align_to(plane, UP)
        for i in range(4):
            self.play(Write(altitude[i]))

        self.play(FadeOut(perpendicular), FadeOut(line_ac),
                  dots[3].animate.set_color(WHITE), labels[3].animate.set_color(WHITE),
                  *[triangles[i].animate.set_stroke(opacity=1).set_fill(opacity=0.2) for i in range(3)],
                  Unwrite(altitude))
        r = (5 ** 0.5) * plane.get_x_unit_size()
        in_circle = Circle(r, color=YELLOW).move_to(points[3])
        radius = Line(points[3], points[3] - np.array([r, 0, 0]), color=YELLOW)
        radius_label = MathTex('r', color=YELLOW, font_size=36).next_to(radius, DOWN / 2)

        self.play(Create(in_circle))
        self.play(Create(radius), Write(radius_label))
        equation = MathTex(r"\frac{\overline{AP}}{\overline{CP}}=\frac{\overline{BP}}{r}",
                           r'\Leftrightarrow r=\sqrt{5}')
        equation.next_to(plane, RIGHT, buff=1).align_to(plane, UP)
        self.play(Write(equation[0]))

        side_lengths_in = MathTex(r'\overline{AP} = \sqrt{7^2+1^2} &= 5 \sqrt{2}\\',
                                  r'\overline{BP} = \sqrt{3^2+1^2} &=  \sqrt{10}\\',
                                  r'\overline{CP} = \sqrt{3^2+4^2} &=  5\\', )
        equation_for_r = MathTex(r'\frac{\overline{AP}}{\overline{CP}}&=\frac{5\sqrt{2}}{5}=\sqrt{2}\\',
                                 r'r&=\overline{BP}\cdot\frac{\overline{CP}}{\overline{AP}}=' +
                                 r'\frac{\sqrt{10}}{\sqrt{2}}=\sqrt{5}')
        side_length_out = MathTex(r'\overline{AC} = &\sqrt{2^2+11^2}=  5\sqrt{5}\\',
                                  r'\overline{AB} = &\sqrt{4^2+8^2} =  4\sqrt{5}\\',
                                  r'\overline{BC} = &\sqrt{3^2+6^2} =  3\sqrt{5}\\', )
        align_to_tex_top(side_lengths_in, equation)
        align_to_tex_top(equation_for_r, side_lengths_in)
        self.play(Write(side_lengths_in))
        self.play(Write(equation_for_r))
        self.play(FadeOut(side_lengths_in), FadeOut(equation_for_r), Write(equation[1]))
        area_equation = MathTex(r'A_{ABC}&=\frac{1}{2}\cdot r \cdot u = 30\\',
                                r'r &= \frac{60}{u} ', r'=\frac{60}{12\sqrt{5}}=\frac{5}{\sqrt{5}} =\sqrt{5}')
        align_to_tex_top(area_equation, equation)
        align_to_tex_top(side_length_out, area_equation)
        self.play(Write(area_equation[:2]))
        self.play(Write(side_length_out))
        self.play(Write(area_equation[2]))

        self.play(*[obj.animate.shift(RIGHT * config.frame_width) for obj in self.mobjects], run_time=2)


class Task641033(Scene):
    def construct(self):
        task_number = Tex('641033').scale(2).center()
        task_underline = Underline(task_number)
        self.play(Create(task_underline), Write(task_number))
        self.play(Uncreate(task_underline), Unwrite(task_number))


class Task641034(Scene):
    def construct(self):
        task_number = Tex('641034').scale(2).center()
        task_underline = Underline(task_number)
        self.play(Create(task_underline), Write(task_number))
        self.play(task_number.animate.to_edge(UP, buff=-2),
                  task_underline.animate.to_edge(UP, buff=-0.5), )

        equations = MathTex(r'x^3+x^2y&=9(x+y)\\', 'y^3+xy^2&=4(x-y)').scale(2)
        self.play(Write(equations[0]), Write(equations[1]))
        self.play(Unwrite(equations[1]), Unwrite(equations[0]))


class Task641035(Scene):
    def construct(self):
        width = config.frame_width
        height = config.frame_height

        task_number = Tex('641035').scale(2).center()
        task_underline = Underline(task_number)
        self.play(Create(task_underline), Write(task_number))
        self.play(task_number.animate.to_edge(UP, buff=-2),
                  task_underline.animate.to_edge(UP, buff=-0.5), )

        plane = NumberPlane(
            x_range=(0, 10, 1),
            y_range=(0, 12, 1),
        ).scale_to_fit_height(height - 2).center()

        _p = 7.058823529411764
        r = 1560 / 289
        coords = {
            'A': (0, 0),  # 0
            'B': (10, 0),  # 1
            'C': (5, 12),  # 2
            'M': (7800 / 3757, 18720 / 3757),  # 3
            'P': (_p, _p),  # 4
            'Q': (5, 2.05882352941),  # 5
            'F': (5, 0)
        }
        points = [plane.c2p(*c) for c in coords.values()]
        dots = [Dot(p) for p in points]
        labels = [
            Text('A').next_to(dots[0], (DOWN + LEFT) / 2),
            Text('B').next_to(dots[1], (DOWN + RIGHT) / 2),
            Text('C').next_to(dots[2], UP / 2),
            Text('M').next_to(dots[3], LEFT / 2),
            Text('P').next_to(dots[4], RIGHT / 2),
            Text('Q').next_to(dots[5], LEFT / 2),
        ]
        circel = Circle(r * plane.get_x_unit_size(), color=RED, ).move_to(points[3])
        # beginne mit zeichnen in A
        radius_mp = Line(points[3], points[4], color=RED)
        radius_ma = Line(points[3], points[0], color=RED)
        angle_p = Angle(Line(points[4], points[2]), radius_mp, dot=True,
                        color=YELLOW, dot_color=YELLOW, quadrant=(1, -1))

        self.play(*[Create(d) for d in dots[:3]], *[Write(l) for l in labels[:3]])
        self.play(Create(Polygon(*points[:3])), Uncreate(task_number), Uncreate(task_underline))
        self.play(Create(dots[3]), Write(labels[3]), Create(circel))
        self.play(Create(radius_mp), Create(dots[4]), Write(labels[4]), Create(radius_ma))
        self.play(Create(angle_p))

        line_pq = Line(points[5], points[4], )
        line_bq = Line(points[5], points[1], )
        angle_q = Angle(line_bq, line_pq, dot=True,
                        color=YELLOW, dot_color=YELLOW, quadrant=(1, 1))

        self.play(Create(dots[5]), Write(labels[5]))
        self.play(Create(line_bq), Create(line_pq), Create(angle_q))

        altitude = Line(points[2], points[6], color=BLUE_B, fill_opacity=0.5, )
        self.play(Create(altitude))

        help_line = Line(points[0], points[4], color=GREEN)
        self.play(Create(help_line))

        self.play(*[obj.animate.shift(DOWN * config.frame_height) for obj in self.mobjects], run_time=2)


class Task641036(Scene):
    def construct(self):
        task_number = Tex('641036').scale(2).center()
        task_underline = Underline(task_number)
        self.play(Create(task_underline), Write(task_number))
        self.play(task_number.animate.to_edge(UP, buff=-2),
                  task_underline.animate.to_edge(UP, buff=-0.5), )

        equation = MathTex(r'w^2+x^2+y^2+z^2=3\cdot 2^n').scale(2)
        self.play(Write(equation))
        self.play(Unwrite(equation))

        finished = Tex('Geschaft!').scale(3).center()
        finished_underline = Underline(finished)

        self.play(Create(finished_underline), Write(finished))
