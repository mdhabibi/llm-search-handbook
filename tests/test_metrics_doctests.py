"""Run the doctests in `metrics` as part of the normal suite.

Without this the `>>>` examples are only checked by someone remembering to run
`python -m doctest src/metrics.py`, and documentation that is not executed
drifts.

Scoped to this one module on purpose. Turning on `--doctest-modules` globally
in pytest.ini would also collect `semantic_search`, whose module docstring
demonstrates the real `SentenceTransformer` encoder -- that example is correct
and worth keeping as documentation, but it downloads a model, so it must not
become a unit test.
"""

import doctest

import metrics


def test_metrics_doctests_pass():
    results = doctest.testmod(metrics, verbose=False)

    assert results.failed == 0, f"{results.failed} doctest example(s) failed"
    # Guards against the examples being deleted and this test quietly passing
    # on an empty module.
    assert results.attempted >= 18
