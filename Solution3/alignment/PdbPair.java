package Solution3.alignment;

public class PdbPair {
    private final String pdbId1;
    private final String pdbId2;

    public PdbPair(String pdbId1, String pdbId2) {
        this.pdbId1 = pdbId1;
        this.pdbId2 = pdbId2;
    }

    public String getPdbId1() {
        return pdbId1;
    }

    public String getPdbId2() {
        return pdbId2;
    }

    @Override
    public String toString() {
        return pdbId1 + " " + pdbId2;
    }
}

