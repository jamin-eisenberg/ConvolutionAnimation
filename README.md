Jamin Eisenberg

EECE 2520

Professor Mohammad Fanaei

6/21/2023

# Convolution Animation Project

CLI tool to produce an explanatory animation of the convolution between two arbitrary functions. I
used [Manim](https://www.manim.community/), an open-source math animation library, to create the animations.

I was inspired by [this video](https://www.youtube.com/watch?v=KuXjwB4LzSA) from 3Blue1Brown.

## Getting Started

If you want to run this project locally, follow these instructions:

1. [Install Manim](https://docs.manim.community/en/stable/installation.html#local-installation). You'll need all the
   required dependencies, plus LaTeX.
2. [Install Python 3.10](https://www.python.org/downloads/) (a lower version may suffice).
3. Clone this repository and navigate to its directory.
4. Read the usage instructions below to create an animation.

## Usage

The script can be run as follows:

```$ main.py <F_LATEX> <F_EXPR> <G_LATEX> <G_EXPR> <FG_PROD_Y_MIN> <FG_PROD_Y_MAX> <T_MIN> <T_MAX> <T_STEP> <ANIMATION_QUALITY>```
where

- f and g are functions of t
- `<X_LATEX>` is a LaTeX string representation of the function
- `<X_EXPR>` is a Python expression representing the value of the function w.r.t. t
- `<FG_PROD_Y_MIN/MAX>` are numbers constituting the range of the product of f and g in the specified domain (this needs
  specification because it is very expensive to calculate at runtime)
- `<T_MIN/MAX/STEP>` are numbers constituting the domain in which you'd like to convolve f and g, and step essentially
  gives the resolution of the function (how often a point is plotted)
- `<ANIMATION_QUALITY>` is one of `low_quality`, `medium_quality`, or `high_quality`, which determines the pixel
  resolution of the output, and also how much time the animation takes to render

See the below for some examples.

## Demo
[dual_triangle_and_rect.mp4](media%2Fvideos%2F480p15%2Fdual_triangle_and_rect.mp4)
