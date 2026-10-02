"""Where an agent's model ends and its effort begins, wherever an agent is written down.

A leaf, and on purpose: `-a` reads an agent through :mod:`hmz.coganchor.backends`, while what
keeps one written down -- a settings file, the interface's sheet -- reads the same word back
without loading every fact about every CLI to do it. Both split it here, so they split it the
same way.
"""

from __future__ import annotations

import re

__all__ = ["parted", "tiered"]

#: What an effort is spelled as, in every CLI's own words: words of letters joined by `-` or a
#: space -- `xhigh`, `extra-high`, `swarmmax`, `as configured`. Read wider than any ladder --
#: any case, `_` as a joint -- so that `High` or `x_high` is still an effort, and refused as
#: one off the ladder rather than run as part of a model nobody has. What follows a model's
#: own `:` is something else -- `gateway/mock/first-model`, `8b` -- and stays the model's.
_EFFORT = re.compile(r"[A-Za-z]+(?:[-_ ][A-Za-z]+)*")

#: What a service tier is spelled as after an effort's `+`: one word -- `fast`, `default`.
#: Read wider than the tiers there are, as an effort is, so that `+Fast` or `+turbo` is still a
#: tier, refused as one by whoever knows the tiers rather than run as part of a model.
_TIER = re.compile(r"[A-Za-z]+")


def parted(said: str) -> tuple[str, str]:
    """What follows an agent's CLI, split into its model and its effort.

    Read from both ends: a model may hold slashes and colons of its own, while an effort never
    does. So the last `:` sets an effort off only where what follows it is spelled as one --
    nothing, or a word, and either of those followed by `+` and the service tier the agent is
    to be served at, as `high+fast` or `auto+fast` -- and is the model's own otherwise:
    MiniMax Code's `custom_provider:gateway/m` is one model, at no effort of its own. A model
    whose own name ends in `:` and a word is written with its effort after it, as
    `qwen3:latest:auto`.

    Args:
      said: `model[:effort[+tier]]`.

    Returns:
      The model, and the effort as written, its tier included: "" where none was, or the `:`
      had nothing after it. :func:`tiered` splits the tier off.
    """
    model, colon, effort = said.rpartition(":")
    if colon and _spelled(effort.strip()):
        return model, effort
    return said, ""


def tiered(effort: str) -> tuple[str, str]:
    """An effort as :func:`parted` gives it, split into its rung and its service tier.

    Args:
      effort: `rung[+tier]`, as written.

    Returns:
      The rung, "" where none was written before the `+`; and the tier, "" where no `+` was
      written at all -- which is no tier asked for, and not the same as asking for `default`.
    """
    rung, plus, tier = effort.partition("+")
    return (rung.strip(), tier.strip()) if plus else (effort.strip(), "")


def _spelled(effort: str) -> bool:
    """Whether what follows the last `:` is an effort, a tier after one, or nothing."""
    rung, plus, tier = effort.partition("+")
    if plus:
        rung = rung.strip()
        return bool(_TIER.fullmatch(tier.strip())) and (
            not rung or bool(_EFFORT.fullmatch(rung))
        )
    return not effort or bool(_EFFORT.fullmatch(effort))
