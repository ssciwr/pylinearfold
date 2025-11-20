import pylinearfold


def test_pylinearfold():
    res = pylinearfold.fold("GGGGAAAACCCC")
    assert res["structure"] == "((((....))))"
    assert res["free_energy"] == -5.4


def test_pylinearpartition():
    res = pylinearfold.partition("GGGGAAAACCCC")
    assert res["structure"] == "((((....))))"
    assert -5.6 < res["free_energy"] < -5.5

    # Probability matrix should only show high probabilities
    # for 0-11, 1-10, 2-9, 3-8 pairs
    bpp = res["probabilities"]
    for i in range(0, 12):
        for j in range(0, 12):
            if i >= j:
                continue
            mask = (bpp["i"] == i) & (bpp["j"] == j)
            filtered = bpp[mask]

            if i + j == 11 and i < 4:
                assert filtered.size == 1
                assert filtered["prob"][0] > 0.8
            else:
                assert filtered.size == 0 or filtered["prob"][0] < 0.2


def test_pylinearpartition_cutoff():
    res = pylinearfold.partition("AUCGGUUCGCCGAU", cutoff=0.7)
    assert res["structure"] == ".((((....))))."
    assert -4.5 < res["free_energy"] < -4.4

    # check that the probabilities are correct
    bpp = res["probabilities"]
    expected_pairs = {1: 12, 2: 11, 3: 10, 4: 9}
    for i in range(14):
        for j in range(14):
            if i >= j:
                continue
            mask = (bpp["i"] == i) & (bpp["j"] == j)
            filtered = bpp[mask]

            if i in expected_pairs and expected_pairs[i] == j:
                assert filtered.size == 1
                assert filtered["prob"][0] > 0.7
            else:
                assert filtered.size == 0 or filtered["prob"][0] < 0.7


def test_pylinearpartition_gamma():
    res = pylinearfold.partition("AUCCGGUUCGCCGGAU", gamma=0.2)
    assert res["structure"] == ".(((((....)))))."
    assert -7.8 < res["free_energy"] < -7.7

    # check that the probabilities are correct
    bpp = res["probabilities"]
    expected_pairs = {1: 14, 2: 13, 3: 12, 4: 11, 5: 10}
    for i in range(16):
        for j in range(16):
            if i >= j:
                continue
            mask = (bpp["i"] == i) & (bpp["j"] == j)
            filtered = bpp[mask]

            if i in expected_pairs and expected_pairs[i] == j:
                assert filtered.size == 1
                assert filtered["prob"][0] > 0.7
            else:
                assert filtered.size == 0 or filtered["prob"][0] < 0.7
