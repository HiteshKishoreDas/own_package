

def rescale_axes(ax, round_decimal=1):
    locs   = ax.get_xticks()
    labels = ax.get_xticklabels()
    for i_l in range(len(labels)):
        labels[i_l].set(text = f"{float(labels[i_l].get_text() )-0.5:.1f}"   )
    ax.set_xticks(locs, labels)

    return ax