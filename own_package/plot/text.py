import matplotlib.patheffects as path_effects


def text_outline(txt_obj, lw=3, color="black"):
    txt_obj.set_path_effects(
        [path_effects.Stroke(linewidth=lw, foreground=color), path_effects.Normal()]
    )


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    txt = ax.text(0.5, 0.5, "Hello World", fontsize=20, color="white")
    text_outline(txt, lw=3, color="black")

    plt.show()
