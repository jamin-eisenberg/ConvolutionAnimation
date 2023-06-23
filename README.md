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

```$ main.py <F_LATEX> <F_EXPR> <G_LATEX> <G_EXPR> <T_MIN> <T_MAX> <T_STEP> <ANIMATION_QUALITY>```
where

- f and g are functions of t
- `<X_LATEX>` is a LaTeX string representation of the function. For tau-subttution to work properly, you must surround
  your dependent variable t with spaces
- `<X_EXPR>` is a Python expression representing the value of the function w.r.t. t
- `<T_MIN/MAX/STEP>` are numbers constituting the domain in which you'd like to convolve f and g, and step essentially
  gives the resolution of the function (how often a point is plotted)
- `<ANIMATION_QUALITY>` is one of `low_quality`, `medium_quality`, or `high_quality`, which determines the pixel
  resolution of the output, and also how much time the animation takes to render

You may need to wait a few minutes for the animation to render, mostly depending on the animation quality and the value
of `<T_STEP>`.

See the below for some examples.

## Demo

`main.py "-\Lambda( t +1)+\Lambda( t -1)" "t if abs(t)<=1 else (-2-t if -2<t<-1 else (2-t if 2>t>1 else 0))" "\Pi(0.2 t )" "1 if abs(t) < 0.2 else 0" -2 2 0.01 low_quality`

https://github.com/jamin-eisenberg/ConvolutionAnimation/assets/117237268/fb376412-d72e-4139-b109-a3523a109021

`main.py "\cos(2 t )\Pi( t )" "math.cos(2*t) if abs(t) <= 0.5 else 0" "10u( t )" "10 if t >= 0 else 0" -4 4 0.01 low_quality`

https://github.com/jamin-eisenberg/ConvolutionAnimation/assets/117237268/1c2d6d71-83ed-4376-a8ae-cdb800795e22

`main.py "e^{-0.5 t }" "math.e**(-0.5 * t)" "2\delta( t -1)" "2 if abs(t - 1) < 0.01 else 0" 0 3 0.005 low_quality`

It's not the prettiest, but I think it gives intuition quite well.

https://github.com/jamin-eisenberg/ConvolutionAnimation/assets/117237268/d52c074b-78ad-45c8-ac00-8cfccbdf7841

## Learning Outcomes

I found that the largest impact of this project on me was helping me to get develop a very good intuition for how the
convolution operation works. I developed this intuition during both the creation of the project and viewing the results.
Actually implementing the convolution operation was a fun exercise that definitely forced me to understand the pieces,
and I think it's useful to see the sliding motion and to see the curve of the product of the two functions, to get a
sense of where the final curve comes from.

During development specifically, I struggled most with auto-ranging and sampling. I know they're not exactly related to
convolution, but working with continuous functions in a discrete way made me think back to some of our discussions at
the very start of the course. It took some work to figure out how to auto-range, especially for a function with a
parameter that changes throughout the animation. That interaction with sampling is also somewhat interesting, as I use
the user-given step value when auto-ranging. This means if a function were to suddenly go to infinity (like 1/t), the
maximum value of the auto-range would be determined based on the step (how close the sample's t value is to 0).

Overall, I thought it was a very useful project for my learning and maybe even for others' learning in the future!