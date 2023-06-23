# so it can be used in given functions
import math

from manim import *

# default space between objects in the scene
DEFAULT_BUFF = 0.5
PLOT_WIDTH = config.frame_width / 2 - DEFAULT_BUFF
TAU_LATEX = r'\tau'


# gets all the floating point numbers between x and y, stepping by jump
def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


# produces a new function from two functions multiplied together
def modulate(f, g):
    return lambda t: f(t) * g(t)


# convolves two functions mechanically
def convolve(f, g, x_opts):
    # takes the mechanical integral w.r.t. tau by summing the product of the function and the step tau takes
    # the bounds of the integral are more than x_min to x_max to avoid seeing chopping for those edge values
    return lambda t: sum(
        [f(tau) * g(t - tau) * x_opts[2] for tau in frange(x_opts[0], x_opts[1], x_opts[2])])


# get an item from a list, but if the index is out of bounds, get the given default instead
def list_get(arr, i, default):
    return arr[i] if 0 <= i < len(arr) else default


# add a Tex title above the given plot
def make_plot_title(plot: Mobject, tex: str):
    title = MathTex(tex).next_to(plot, direction=UP, buff=DEFAULT_BUFF / 2)
    title.scale_to_fit_width(min(title.width, PLOT_WIDTH))
    return title


# gets the range of a function in the given domain
def get_func_range(func: Callable[[float], float], x_opts: (float, float, float)):
    func_vals = [func(x) for x in frange(*x_opts)]
    return [min(func_vals) - 0.005, max(func_vals) + 0.005]  # if the function is fully flat, add some dimension


# plots the given function f with the given color and the given x options and y-range, and returns
# the axes the function was plotted on (transformed by axes_func) and the function itself
def plot(f, f_color, x_opts, axes_func, y_range=None, **kwargs) -> (Axes, Mobject):
    axes_options = {'x_range': x_opts, 'tips': False, 'x_length': PLOT_WIDTH,
                    'y_length': config.frame_height / 6, 'axis_config': {"include_ticks": False},
                    'y_range': y_range or get_func_range(f, x_opts)} | kwargs
    axes = axes_func(Axes(**axes_options))
    graph = axes.plot(f, color=f_color, use_smoothing=False)
    return axes, graph


# represents a scene that animates a convolution
class AnimatedConvolution(Scene):
    # eq1 and eq2 are evaluated strings representing the functions being convolved
    # their _str counterparts are the title of the function that should be displayed
    # x_opts is an array of [x_min, x_max, x_step] used for plotting all functions
    # prod_y_range provides a range in which to display the product of the functions, as that is difficult to
    # pre-calculate
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

    # creates the components for and plays the scene
    def construct(self):
        # creates the plot of f (eq1) in the top left corner, in red
        axf, graphf = plot(self.eq1, RED, self.x_opts,
                           lambda x: x.move_to(UP * (config.frame_height * 7 / 24) + LEFT * (config.frame_width / 4)))
        # establishes f's two titles, one with t and one with tau
        titlef1 = make_plot_title(axf, f"f(t) = {self.eq1_str}")
        titlef2 = make_plot_title(axf, rf"f({TAU_LATEX}) = {self.eq1_str.replace('t', TAU_LATEX)}")

        # sets up the value used to change the position of g (eq2) and the shape of f times g
        t = ValueTracker(0)
        # sets up the second (reversed) value of the function g
        g2_func = lambda tau: self.eq2(t.get_value() - tau)
        # get the range of g when t = 0
        g2_range = get_func_range(g2_func, self.x_opts)
        # prepare t for sweeping from x_min to x_max
        t = ValueTracker(self.x_min)

        def plot_g2():
            return plot(g2_func, BLUE, self.x_opts,
                        lambda x: x.next_to(axf, direction=DOWN, buff=3 * DEFAULT_BUFF), y_range=g2_range)

        # plot g1 under f
        axg, graphg1 = plot(self.eq2, BLUE, self.x_opts,
                            lambda x: x.next_to(axf, direction=DOWN, buff=3 * DEFAULT_BUFF))
        _, graphg2 = plot_g2()
        # prepare each title of g, with t, tau, and t-tau
        titleg1 = make_plot_title(axg, f"g(t) = {self.eq2_str}")
        titleg2 = make_plot_title(axg, rf"g({TAU_LATEX}) = {self.eq2_str.replace('t', TAU_LATEX)}")
        titleg3 = make_plot_title(axg, rf"g(t-{TAU_LATEX}) = {self.eq2_str.replace('t', f'(t-{TAU_LATEX})')}")

        # get the product function (relying on the value t)
        prod_func = modulate(self.eq1, lambda tau: self.eq2(t.get_value() - tau))

        def plot_prod():
            return plot(prod_func, GREEN,
                        self.x_opts, lambda x: x.next_to(axg, direction=DOWN, buff=3 * DEFAULT_BUFF),
                        y_range=self.prod_y_range)

        ax_prod, graph_prod = plot_prod()

        # add dependency of g2 and the product plot on t, so they update when t changes
        graphg2.add_updater(lambda func: func.become(plot_g2()[1]))
        graph_prod.add_updater(lambda func: func.become(plot_prod()[1]))

        title_prod = make_plot_title(ax_prod, f"f({TAU_LATEX})g(t-{TAU_LATEX})")

        # plot the convolution of the functions on the right
        convolution_func = convolve(self.eq1, self.eq2, self.x_opts)
        ax_conv, graph_conv = plot(convolution_func, PURPLE, self.x_opts,
                                   lambda x: x.move_to(RIGHT * config.frame_width / 4), y_length=4)

        # just display the definition (symbolic calculation would be crazy)
        convolution_def_latex = rf"(f \ast g)(t)=\int_{{-\infty}}^{{\infty}} f({TAU_LATEX}) g(t-{TAU_LATEX}) d {TAU_LATEX}"
        title_conv = make_plot_title(ax_conv, convolution_def_latex)

        # animate the creation of all the axes and the plots that are shown initially
        self.play(*map(Create, [titlef1, axf, titleg1, axg, title_prod, ax_prod, title_conv, ax_conv]))
        self.play(Create(graphf), Create(graphg1))

        # animate the transformation of the titles and g2 - substituting tau for t, then negating tau
        self.play(Transform(titlef1, titlef2))
        self.play(ReplacementTransform(titleg1, titleg2))
        self.play(ReplacementTransform(titleg2, titleg3), ReplacementTransform(graphg1, graphg2))

        # animate sweeping t through the x-domain
        self.add(graph_prod)
        self.add(graph_conv)
        self.play(t.animate.set_value(self.x_max), Create(graph_conv), rate_func=linear, run_time=8)

        # revert t to 0
        self.play(t.animate.set_value(0))


def main():
    if not 7 <= len(sys.argv) <= 11:
        print('Invalid command line arguments. Please consult the README.')
        return

    with tempconfig(
            {"quality": list_get(sys.argv, 10, "medium_quality"), "preview": True, }):
        try:
            prod_y_min = float(sys.argv[5])
            prod_y_max = float(sys.argv[6])
            x_min = float(sys.argv[7])
            x_max = float(sys.argv[8])
            x_step = float(sys.argv[9])
        except ValueError:
            print('The x-domain and y-range values must be numbers. Please consult the README.')
            return

        scene = AnimatedConvolution(sys.argv[2], sys.argv[4], sys.argv[1], sys.argv[3], [x_min, x_max, x_step],
                                    [prod_y_min, prod_y_max])
        scene.render()


if __name__ == '__main__':
    main()
