from dift.core.quality_diff import classify_null_spike


def test_null_spike_low():
    is_spike, severity = classify_null_spike(2.5)

    assert is_spike is False
    assert severity == "low"


def test_null_spike_medium():
    is_spike, severity = classify_null_spike(7.0)

    assert is_spike is True
    assert severity == "medium"


def test_null_spike_high():
    is_spike, severity = classify_null_spike(20.0)

    assert is_spike is True
    assert severity == "high"
