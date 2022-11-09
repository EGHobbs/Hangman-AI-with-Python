from manim import *


class HangmanGallows(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        self.camera.frame.set(width=4, height=6).move_to([-2, 1, 0])
        line = Line().move_to([-3, -1, 0])
        line.width = 1
        small_line = line.copy()
        small_line.width = 0.5
        self.play(Create(line), Create(line.copy()), run_time=0.5)
        self.play(line.animate.rotate(PI / 2, about_edge=line.start), run_time=0.75)
        self.add(line.copy())
        self.play(
            line.copy().animate.rotate(PI / 2, about_edge=DOWN),
            Rotate(line, angle=PI, about_point=line.get_end()),
            run_time=0.75,
        )
        self.add(line.copy())
        self.play(Rotate(line, angle=-PI, about_point=line.get_start()), run_time=0.75)
        self.add(line.copy(), small_line)
        self.play(
            Rotate(line, angle=PI, about_point=line.get_end()),
            small_line.animate.put_start_and_end_on(([-3.5, 0, 0]), ([-3, -1, 0])),
            run_time=0.75,
        )
        self.add(line.copy(), small_line.copy())
        self.play(
            line.animate.rotate(PI / 2, about_edge=UP),
            small_line.animate.put_start_and_end_on(([-3.5, 0, 0]), ([-4, -1, 0])),
            run_time=0.75,
        )
        small_l2 = line.copy()
        small_l2.width = 0.5
        self.add(line.copy(), small_l2)
        self.play(
            line.animate.rotate(PI, about_edge=RIGHT),
            small_l2.animate.put_start_and_end_on(([-3.5, 2.5, 0]), ([-3, 3, 0])),
            run_time=0.75,
        )
        self.add(line.copy())
        self.play(line.animate.rotate(PI / 2, about_edge=RIGHT), run_time=0.75)
        self.play(Restore(self.camera.frame))


class Hangman(Scene):
    head = (
        Circle(radius=0.25, color=WHITE).move_to(UP * 1.75 + LEFT * 1.5).rotate(PI / 2)
    )
    torso = Line(start=UP * 0.75, end=ORIGIN).next_to(head, direction=DOWN, buff=0)
    arms = Line(start=RIGHT * 0.5, end=ORIGIN).next_to(head, direction=DOWN, buff=0.25)
    left_leg = Line(start=[-0.25, 0.5, 0], end=ORIGIN).next_to(
        torso, direction=DR, buff=0
    )
    right_leg = Line(start=[0.25, 0.5, 0], end=ORIGIN).next_to(
        torso, direction=DL, buff=0
    )
    left_eye = (
        Cross(scale_factor=0.05, stroke_color=WHITE, stroke_width=3)
        .next_to(head, direction=ORIGIN, buff=0)
        .shift(UR * 0.075)
    )
    right_eye = (
        Cross(scale_factor=0.05, stroke_color=WHITE, stroke_width=3)
        .next_to(head, direction=ORIGIN, buff=0)
        .shift(UL * 0.075)
    )
    mouth = Line(start=right_eye.get_center(), end=left_eye.get_center()).shift(
        DOWN * 0.15
    )
    man = VGroup(head, torso, arms, right_leg, left_leg, right_eye, left_eye, mouth)

    def also_add_to_man(self, vgroup=VGroup(), text_object=Text("a"), index=0):
        self.play(
            text_object.animate.set_color(RED).scale(1.5),
            Create(vgroup[index]),
            runtime=0.5,
        )

    def also_remove_man(self, vgroup=VGroup(), text_object=Text("a")):
        self.play(
            text_object.animate.set_color(RED).scale(1.5),
            FadeOut(vgroup, shift=UP * 0.25),
            runtime=0.5,
        )

    def just_enlarge_red(self, text_object=Text("a")):
        self.play(text_object.animate.set_color(RED).scale(1.5), runtime=0.5)

    def shrink_and_remove(self, text_object=Text("a")):
        self.play(text_object.animate.set_color(WHITE).scale(0.66), runtime=0.5)
        self.play(FadeOut(text_object, shift=UP * 0.25))

    def create_underlines(self, hangman):
        if hangman.size < 13:
            underlines = VGroup(
                *[Line(start=LEFT * 0.75, end=ORIGIN) for _ in range(hangman.size)]
            )
            underlines.arrange(buff=0.25).shift(DOWN * 3)
        else:
            underlines = VGroup(
                *[
                    Line(start=LEFT * 0.75 * 12 / hangman.size, end=ORIGIN)
                    for _ in range(hangman.size)
                ]
            )
            underlines.arrange(buff=0.25 * 12 / hangman.size).shift(DOWN * 3)
        self.play(Create(underlines))
        return underlines

    def create_letter(self, text="a"):
        Text.set_default(font_size=100)
        l = Text(text.upper()).shift(RIGHT * 3 + UP)
        self.play(Write(l))
        return l
