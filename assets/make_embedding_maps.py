# -*- coding: utf-8 -*-
"""Generate the Chapter 4 embedding-map figures.

Embeds our own example words and sentences with `all-MiniLM-L6-v2`, projects the
384-dimensional vectors down to 2-D / 3-D, and writes four PNGs into `assets/`:

    embeddings-qa-map.png        questions landing beside their answers (UMAP, 2-D)
    embeddings-atlas-2d.png      a semantic atlas of ~150 terms  (UMAP, 2-D)
    embeddings-atlas-3d.png      the same atlas in 3-D           (UMAP, 3-D)
    embeddings-umap-vs-pca.png   the same vectors, both methods, side by side

Run once from the repo root:

    python assets/make_embedding_maps.py

Needs `sentence-transformers` (downloads a ~90 MB model on first run) and, ideally,
`umap-learn`. Without UMAP the script still works and falls back to PCA everywhere,
printing a note.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.decomposition import PCA

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 42

# ---------------------------------------------------------------- brand palette
INDIGO = "#1E3A8A"
BLUE = "#2563EB"
VIOLET = "#7C3AED"
INK = "#0F172A"
MUTED = "#64748B"
PAPER = "#F8FAFF"
GRID = "#E2E8F0"

THEME_COLORS = [
    "#2563EB",  # blue
    "#7C3AED",  # violet
    "#059669",  # emerald
    "#D97706",  # amber
    "#DC2626",  # red
    "#0891B2",  # cyan
    "#DB2777",  # pink
    "#65A30D",  # lime
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": GRID,
    "axes.labelcolor": MUTED,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

# ------------------------------------------------------------------- our data
# 1) Question/answer pairs, built on the themes of the course corpus.
QA_PAIRS = [
    ("What colour is the grass?",          "Grass is green because of chlorophyll."),
    ("Why does the sky look blue?",        "The sky appears blue due to Rayleigh scattering."),
    ("What causes a migraine?",            "A migraine is a throbbing pain on one side of the head."),
    ("Is a whale a fish?",                 "A whale is a mammal, not a fish."),
    ("How do I make my laptop last longer?","Battery life improves when you dim the screen."),
    ("Where do penguins live?",            "Penguins live on the Antarctic coast."),
    ("What is the capital of Canada?",     "Ottawa is the capital city of Canada."),
    ("How does an engine work?",           "An engine burns fuel to drive pistons."),
    ("What is photosynthesis?",            "Plants convert sunlight into chemical energy."),
    ("How deep is the ocean?",             "The Mariana Trench reaches nearly 11 kilometres down."),
]

# 2) A semantic atlas: our own vocabulary across eight everyday themes.
ATLAS = {
    "Fruit": [
        "apple", "banana", "orange", "mango", "strawberry", "pineapple", "grape",
        "peach", "watermelon", "cherry", "lemon", "blueberry", "pear", "apricot",
        "raspberry", "kiwi", "plum", "fig",
    ],
    "Vehicles": [
        "car", "bus", "bicycle", "motorcycle", "truck", "train", "tram", "scooter",
        "aeroplane", "helicopter", "ferry", "submarine", "tractor", "van",
        "ambulance", "taxi", "sailboat", "canoe",
    ],
    "Buildings": [
        "house", "castle", "cathedral", "skyscraper", "cottage", "barn", "lighthouse",
        "museum", "library", "stadium", "hospital", "warehouse", "temple", "tower",
        "bungalow", "palace", "cabin", "bridge",
    ],
    "Sports": [
        "football", "tennis", "cricket", "basketball", "swimming", "boxing", "rugby",
        "golf", "cycling", "marathon", "surfing", "skiing", "rowing", "archery",
        "fencing", "badminton", "gymnastics", "judo",
    ],
    "Music": [
        "guitar", "piano", "violin", "drums", "trumpet", "flute", "cello", "saxophone",
        "harp", "clarinet", "banjo", "accordion", "orchestra", "symphony", "melody",
        "chord", "rhythm", "concert",
    ],
    "Weather": [
        "rain", "snow", "thunderstorm", "fog", "hurricane", "drought", "blizzard",
        "sunshine", "hail", "humidity", "monsoon", "frost", "breeze", "lightning",
        "tornado", "overcast", "heatwave", "drizzle",
    ],
    "Programming": [
        "python", "javascript", "compiler", "database", "algorithm", "debugging",
        "recursion", "variable", "function", "repository", "framework", "runtime",
        "syntax", "refactor", "pointer", "container", "interface", "kernel",
    ],
    "Cooking": [
        "roasting", "simmer", "marinate", "whisk", "saucepan", "recipe", "seasoning",
        "baking", "chopping", "frying", "oven", "dough", "garnish", "casserole",
        "grill", "knead", "sauté", "broth",
    ],
}

# Terms that deliberately sit between themes, to show the map is continuous.
BRIDGES = ["apple pie", "racing car", "football stadium", "storm cloud", "piano lesson"]


# ------------------------------------------------------------------- machinery
def embed(texts):
    """Encode texts with the course model. Returns an (n, 384) float array."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return np.asarray(model.encode(list(texts), show_progress_bar=False))


def project(vectors, n_components=2, n_neighbors=12, min_dist=0.25):
    """UMAP if available, otherwise PCA. Returns (coords, method_name)."""
    try:
        import umap  # noqa: F401  (umap-learn)
    except ImportError:
        return PCA(n_components=n_components, random_state=SEED).fit_transform(vectors), "PCA"
    import umap
    n_neighbors = max(2, min(n_neighbors, len(vectors) - 1))
    reducer = umap.UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric="cosine",
        random_state=SEED,
    )
    return reducer.fit_transform(vectors), "UMAP"


def _clean(ax, keep_ticks=False):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_facecolor(PAPER)
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    if not keep_ticks:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(length=0)


def spread_labels(fig, ax, annotations, iterations=60, step=1.4):
    """Nudge annotations vertically until they stop overlapping.

    Embedding pairs land close together by design, so their captions collide. We
    measure the rendered text boxes and push overlapping ones apart along y,
    keeping each label near its own point.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for _ in range(iterations):
        boxes = [a.get_window_extent(renderer=renderer) for a in annotations]
        moved = False
        for i in range(len(annotations)):
            for j in range(i + 1, len(annotations)):
                bi, bj = boxes[i], boxes[j]
                if not bi.overlaps(bj):
                    continue
                moved = True
                # push the higher one up and the lower one down
                up, down = (i, j) if bi.y0 >= bj.y0 else (j, i)
                for idx, sign in ((up, +1), (down, -1)):
                    x, y = annotations[idx].get_position()
                    annotations[idx].set_position((x, y + sign * step))
        if not moved:
            break
        fig.canvas.draw()
        boxes = [a.get_window_extent(renderer=renderer) for a in annotations]


def save(fig, name):
    path = os.path.join(HERE, name)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", os.path.relpath(path, os.path.dirname(HERE)))


# --------------------------------------------------------------------- figures
def figure_qa_map():
    """Every question lands beside its own answer."""
    texts, kinds, pair_ids = [], [], []
    for i, (q, a) in enumerate(QA_PAIRS):
        texts += [q, a]
        kinds += ["q", "a"]
        pair_ids += [i, i]

    vecs = embed(texts)
    # Deliberately PCA, not UMAP. This figure makes a claim about *distance*
    # ("the answer is the nearest point to its question"), and PCA preserves
    # distances while UMAP distorts them. UMAP also needs a decent number of
    # points to build a neighbour graph -- with 20 it produces arbitrary layouts.
    xy = PCA(n_components=2, random_state=SEED).fit_transform(vecs)
    method = "PCA"

    fig, ax = plt.subplots(figsize=(14, 9))
    _clean(ax)

    # join each question to its answer
    for i in range(len(QA_PAIRS)):
        idx = [j for j, p in enumerate(pair_ids) if p == i]
        ax.plot(xy[idx, 0], xy[idx, 1], color=MUTED, linewidth=1.1,
                alpha=0.55, zorder=1, linestyle="--")

    annotations = []
    for j, kind in enumerate(kinds):
        is_q = kind == "q"
        ax.scatter(xy[j, 0], xy[j, 1], s=190,
                   c=BLUE if is_q else VIOLET,
                   marker="o" if is_q else "s",
                   edgecolors="white", linewidths=1.6, zorder=3)
        label = texts[j]
        if len(label) > 36:
            label = label[:33] + "…"
        # questions label upward, answers downward: pairs sit close together, so
        # splitting the direction keeps the two captions apart to begin with.
        dy, va = (15, "bottom") if is_q else (-16, "top")
        ann = ax.annotate(
            label, (xy[j, 0], xy[j, 1]),
            textcoords="offset points", xytext=(0, dy),
            ha="center", va=va, fontsize=8,
            color=INK if is_q else VIOLET, zorder=5,
            # a soft backing box keeps text legible wherever labels still cross
            bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                      edgecolor="none", alpha=0.82),
        )
        annotations.append(ann)

    # resolve any remaining collisions
    spread_labels(fig, ax, annotations)

    ax.set_title("Questions land beside their own answers",
                 fontsize=17, fontweight="bold", color=INK, pad=16)
    ax.text(0.5, 1.015,
            f"{len(QA_PAIRS)} question/answer pairs · 384-D embeddings projected to 2-D with "
            f"{method} (distance-preserving)",
            transform=ax.transAxes, ha="center", fontsize=10, color=MUTED)
    ax.legend(handles=[
        Line2D([], [], marker="o", linestyle="", color=BLUE, markersize=10,
               markeredgecolor="white", label="question"),
        Line2D([], [], marker="s", linestyle="", color=VIOLET, markersize=10,
               markeredgecolor="white", label="answer"),
        Line2D([], [], linestyle="--", color=MUTED, label="same pair"),
    ], loc="best", frameon=False, fontsize=10)
    save(fig, "embeddings-qa-map.png")
    return vecs


def _atlas_data():
    texts, themes = [], []
    for theme, words in ATLAS.items():
        texts += words
        themes += [theme] * len(words)
    texts += BRIDGES
    themes += ["Between themes"] * len(BRIDGES)
    return texts, themes


def figure_atlas_2d(vecs, texts, themes):
    xy, method = project(vecs, n_components=2, n_neighbors=12, min_dist=0.25)
    names = list(ATLAS.keys())

    fig, ax = plt.subplots(figsize=(13, 9))
    _clean(ax)

    for k, theme in enumerate(names):
        idx = [i for i, t in enumerate(themes) if t == theme]
        ax.scatter(xy[idx, 0], xy[idx, 1], s=120, c=THEME_COLORS[k],
                   edgecolors="white", linewidths=1.1, label=theme, zorder=3)
        # label each cluster just above its points, so the text never sits on them
        cx = xy[idx, 0].mean()
        top = xy[idx, 1].max()
        pad = 0.035 * (xy[:, 1].max() - xy[:, 1].min())
        ax.text(cx, top + pad, theme.upper(), fontsize=12.5, fontweight="bold",
                color=THEME_COLORS[k], ha="center", va="bottom", alpha=0.85, zorder=6)

    idx = [i for i, t in enumerate(themes) if t == "Between themes"]
    ax.scatter(xy[idx, 0], xy[idx, 1], s=150, facecolors="none",
               edgecolors=INK, linewidths=1.8, label="between themes", zorder=4)
    for i in idx:
        ax.annotate(texts[i], (xy[i, 0], xy[i, 1]), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=8.5,
                    color=INK, fontweight="bold", zorder=5)

    ax.set_title("A semantic atlas: meaning becomes location",
                 fontsize=18, fontweight="bold", color=INK, pad=16)
    ax.text(0.5, 1.015,
            f"{len(texts)} everyday terms · 384-D embeddings projected to 2-D with {method} "
            f"· nobody told the model these categories",
            transform=ax.transAxes, ha="center", fontsize=10, color=MUTED)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=10)
    save(fig, "embeddings-atlas-2d.png")


def figure_atlas_3d(vecs, themes):
    xyz, method = project(vecs, n_components=3, n_neighbors=12, min_dist=0.25)
    names = list(ATLAS.keys())

    fig = plt.figure(figsize=(12.5, 9))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")

    for k, theme in enumerate(names):
        idx = [i for i, t in enumerate(themes) if t == theme]
        ax.scatter(xyz[idx, 0], xyz[idx, 1], xyz[idx, 2], s=70,
                   c=THEME_COLORS[k], edgecolors="white", linewidths=0.6,
                   label=theme, depthshade=True)

    idx = [i for i, t in enumerate(themes) if t == "Between themes"]
    ax.scatter(xyz[idx, 0], xyz[idx, 1], xyz[idx, 2], s=110,
               facecolors="none", edgecolors=INK, linewidths=1.6,
               label="between themes")

    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.set_pane_color((1, 1, 1, 1))
        pane.line.set_color(GRID)
        pane.set_ticklabels([])
    ax.grid(True, color=GRID)
    ax.view_init(elev=22, azim=-60)

    ax.set_title("The same atlas in three dimensions\n"
                 f"(real embeddings have 384 — {method} keeps the neighbourhoods)",
                 fontsize=15, fontweight="bold", color=INK, pad=22)
    ax.legend(loc="upper left", bbox_to_anchor=(-0.02, 0.92), frameon=False, fontsize=9)
    save(fig, "embeddings-atlas-3d.png")


def figure_umap_vs_pca(vecs, themes):
    names = list(ATLAS.keys())
    try:
        import umap
        reducer = umap.UMAP(n_components=2, n_neighbors=12, min_dist=0.25,
                            metric="cosine", random_state=SEED)
        left, left_name = reducer.fit_transform(vecs), "UMAP"
    except ImportError:
        left, left_name = PCA(n_components=2, random_state=SEED).fit_transform(vecs), "PCA"
    right = PCA(n_components=2, random_state=SEED).fit_transform(vecs)

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    for ax, coords, name in ((axes[0], left, left_name), (axes[1], right, "PCA")):
        _clean(ax)
        for k, theme in enumerate(names):
            idx = [i for i, t in enumerate(themes) if t == theme]
            ax.scatter(coords[idx, 0], coords[idx, 1], s=70, c=THEME_COLORS[k],
                       edgecolors="white", linewidths=0.7, label=theme)
        idx = [i for i, t in enumerate(themes) if t == "Between themes"]
        ax.scatter(coords[idx, 0], coords[idx, 1], s=95, facecolors="none",
                   edgecolors=INK, linewidths=1.5)
        ax.set_title(name, fontsize=15, fontweight="bold", color=INK)

    axes[0].text(0.5, -0.07, "separates neighbourhoods clearly —\nbut distance *between* clusters means little",
                 transform=axes[0].transAxes, ha="center", fontsize=9.5, color=MUTED)
    axes[1].text(0.5, -0.07, "a faithful linear shadow —\nglobal layout honest, clusters overlap more",
                 transform=axes[1].transAxes, ha="center", fontsize=9.5, color=MUTED)
    axes[1].legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=9.5)

    fig.suptitle("Two ways to flatten 384 dimensions onto a page",
                 fontsize=17, fontweight="bold", color=INK, y=1.0)
    save(fig, "embeddings-umap-vs-pca.png")


def main():
    try:
        import umap  # noqa: F401
    except ImportError:
        print("NOTE: umap-learn not installed — falling back to PCA for every figure.\n"
              "      Install it with:  pip install umap-learn\n")

    print("embedding question/answer pairs …")
    figure_qa_map()

    print("embedding the semantic atlas …")
    texts, themes = _atlas_data()
    vecs = embed(texts)

    figure_atlas_2d(vecs, texts, themes)
    figure_atlas_3d(vecs, themes)
    figure_umap_vs_pca(vecs, themes)
    print("\ndone — four figures written to assets/")


if __name__ == "__main__":
    sys.exit(main())
