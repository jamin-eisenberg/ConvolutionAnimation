from manim import *

DEFAULT_BUFF = 0.5
PLOT_WIDTH = config.frame_width / 2 - DEFAULT_BUFF
TAU_LATEX = r'\tau'


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def modulate(f, g):
    return lambda t: f(t) * g(t)


def convolve(f, g, x_opts):
    return lambda t: sum(
        [f(tau) * g(t - tau) * x_opts[2] for tau in frange(x_opts[0] - x_opts[1], x_opts[1] - x_opts[0], x_opts[2])])


def list_get(arr, i, default):
    return arr[i] if 0 <= i < len(arr) else default


def make_plot_title(plot: Mobject, tex: str):
    title = MathTex(tex).next_to(plot, direction=UP, buff=DEFAULT_BUFF / 2)
    title.scale_to_fit_width(min(title.width, PLOT_WIDTH))
    return title


def get_func_range(func: Callable[[float], float], x_opts: (float, float, float)):
    func_vals = [func(x) for x in frange(*x_opts)]
    return [min(func_vals) - 0.005, max(func_vals) + 0.005]  # if the function is fully flat, add some dimension


def plot(f, f_color, x_opts, axes_func, y_range=None, **kwargs) -> (Axes, Mobject):
    axes_options = {'x_range': x_opts, 'tips': False, 'x_length': PLOT_WIDTH,
                    'y_length': config.frame_height / 6, 'axis_config': {"include_ticks": False},
                    'y_range': y_range or get_func_range(f, x_opts)} | kwargs
    axes = axes_func(Axes(**axes_options))
    graph = axes.plot(f, color=f_color, use_smoothing=False)
    return axes, graph


class AnimatedConvolution(Scene):
    def __init__(self, eq1, eq2, eq1_str: str, eq2_str: str, x_opts: [float, float, float],
                 prod_y_range: [float, float]):
        super().__init__()
        self.eq1 = eval("lambda t: " + eq1)
        self.eq2 = eval("lambda t: " + eq2)
        self.eq1_str = eq1_str
        self.eq2_str = eq2_str
        self.x_min, self.x_max, self.x_step = x_opts
        self.x_opts = x_opts
        self.prod_y_range = prod_y_range

    def construct(self):
        axf, graphf = plot(self.eq1, RED, self.x_opts,
                           lambda x: x.move_to(UP * (config.frame_height * 7 / 24) + LEFT * (config.frame_width / 4)))
        titlef1 = make_plot_title(axf, f"f(t) = {self.eq1_str}")
        titlef2 = make_plot_title(axf, rf"f({TAU_LATEX}) = {self.eq1_str.replace('t', TAU_LATEX)}")

        t = ValueTracker(0)
        g2_func = lambda tau: self.eq2(t.get_value() - tau)
        g2_range = get_func_range(g2_func, self.x_opts)
        t = ValueTracker(self.x_min)

        def plot_g2():
            return plot(g2_func, BLUE, self.x_opts,
                        lambda x: x.next_to(axf, direction=DOWN, buff=3 * DEFAULT_BUFF), y_range=g2_range)

        axg, graphg1 = plot(self.eq2, BLUE, self.x_opts,
                            lambda x: x.next_to(axf, direction=DOWN, buff=3 * DEFAULT_BUFF))
        _, graphg2 = plot_g2()
        titleg1 = make_plot_title(axg, f"g(t) = {self.eq2_str}")
        titleg2 = make_plot_title(axg, rf"g({TAU_LATEX}) = {self.eq2_str.replace('t', TAU_LATEX)}")
        titleg3 = make_plot_title(axg, rf"g(t-{TAU_LATEX}) = {self.eq2_str.replace('t', f'(t-{TAU_LATEX})')}")

        prod_func = modulate(self.eq1, lambda tau: self.eq2(t.get_value() - tau))

        def plot_prod():
            return plot(prod_func, GREEN,
                        self.x_opts, lambda x: x.next_to(axg, direction=DOWN, buff=3 * DEFAULT_BUFF),
                        y_range=self.prod_y_range)

        ax_prod, graph_prod = plot_prod()

        graph_prod.add_updater(lambda func: func.become(plot_prod()[1]))
        graphg2.add_updater(lambda func: func.become(plot_g2()[1]))

        title_prod = make_plot_title(ax_prod, f"f({TAU_LATEX})g(t-{TAU_LATEX})")

        convolution_func = convolve(self.eq1, self.eq2, self.x_opts)
        ax_conv, graph_conv = plot(convolution_func, PURPLE, self.x_opts,
                                   lambda x: x.move_to(RIGHT * config.frame_width / 4), y_length=4)

        convolution_def_latex = rf"(f \ast g)(t)=\int_{{-\infty}}^{{\infty}} f({TAU_LATEX}) g(t-{TAU_LATEX}) d {TAU_LATEX}"
        title_conv = make_plot_title(ax_conv, convolution_def_latex)

        self.play(*map(Create, [titlef1, axf, titleg1, axg, title_prod, ax_prod, title_conv, ax_conv]))
        self.play(Create(graphf), Create(graphg1))

        self.play(Transform(titlef1, titlef2))
        self.play(ReplacementTransform(titleg1, titleg2))
        self.play(ReplacementTransform(titleg2, titleg3), ReplacementTransform(graphg1, graphg2))

        self.add(graph_prod)
        self.add(graph_conv)
        self.play(t.animate.set_value(self.x_max), Create(graph_conv), rate_func=linear, run_time=8)
        self.play(t.animate.set_value(0))

        # graph22_copy = graphg2.copy()
        # graph2_guideline = Line(axg.coords_to_point(convolution_x_opts[0], 0),
        #                         axg.coords_to_point(convolution_x_opts[1], 0))
        # self.play(MoveAlongPath(graphg2, graph2_guideline), Create(graph_conv), Create(graph_prod), rate_func=linear,
        #           run_time=8)
        # graphg2.target = graph22_copy
        # self.play(MoveToTarget(graphg2))


def main():
    if not 7 <= len(sys.argv) <= 10:
        print('Invalid command line arguments. Please consult the README.')
        return

    with tempconfig(
            {"quality": "low_quality", "preview": True, }):
        try:
            prod_y_min = float(list_get(sys.argv, 5, "no default"))
            prod_y_max = float(list_get(sys.argv, 6, "no default"))
            x_min = float(list_get(sys.argv, 7, "-2"))
            x_max = float(list_get(sys.argv, 8, "2"))
            x_step = float(list_get(sys.argv, 9, "0.1"))
        except ValueError:
            print('The x-domain values must be numbers. Please consult the README.')
            return

        scene = AnimatedConvolution(sys.argv[2], sys.argv[4], sys.argv[1], sys.argv[3], [x_min, x_max, x_step],
                                    [prod_y_min, prod_y_max])
        scene.render()


if __name__ == '__main__':
    main()
