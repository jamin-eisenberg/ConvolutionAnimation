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
- `<X_LATEX>` is a LaTeX string representation of the function. For tau-subttution to work properly, you must surround your dependent variable t with spaces
- `<X_EXPR>` is a Python expression representing the value of the function w.r.t. t
- `<FG_PROD_Y_MIN/MAX>` are numbers constituting the range of the product of f and g in the specified domain (this needs
  specification because it is very expensive to calculate at runtime)
- `<T_MIN/MAX/STEP>` are numbers constituting the domain in which you'd like to convolve f and g, and step essentially
  gives the resolution of the function (how often a point is plotted)
- `<ANIMATION_QUALITY>` is one of `low_quality`, `medium_quality`, or `high_quality`, which determines the pixel
  resolution of the output, and also how much time the animation takes to render

You may need to wait a few minutes for the animation to render, mostly depending on the animation quality and the value of `<T_STEP>`.

See the below for some examples.

## Demo
`main.py "-\Lambda( t +1)+\Lambda( t -1)" "t if abs(t)<=1 else (-2-t if -2<t<-1 else (2-t if 2>t>1 else 0))" "\Pi(0.2 t )" "1 if abs(t) < 0.2 else 0" -1.25 1.25 -2 2 0.01 low_quality`

https://github.com/jamin-eisenberg/ConvolutionAnimation/assets/117237268/fb376412-d72e-4139-b109-a3523a109021



`main.py "\cos(2 t )\Pi( t )" "math.cos(2*t) if abs(t) <= 0.5 else 0" "10u( t )" "10 if t >= 0 else 0" -11 11 -4 4 0.01 low_quality`

https://github.com/jamin-eisenberg/ConvolutionAnimation/assets/117237268/1c2d6d71-83ed-4376-a8ae-cdb800795e22



`main.py "e^{-0.5 t }" "math.e**(-0.5 * t)" "2\delta( t -1)" "2 if abs(t - 1) < 0.01 else 0" 0 1.5 0 3 0.01 low_quality` 

https://github.com/jamin-eisenberg/ConvolutionAnimation/assets/117237268/66dd4582-a46d-44b0-9f4c-3c7a5da5afb2

(FIX)

