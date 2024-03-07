package Solution3.alignment;

public class PdbSequence {
    private final String pdbId;
    private final String pdbSequence;

    public PdbSequence(String pdbId, String pdbSequence) {
        this.pdbId = pdbId;
        this.pdbSequence = pdbSequence;
    }

    public String getPdbId() {
        return pdbId;
    }

    public String getPdbSequence() {
        return pdbSequence;
    }

    @Override
    public String toString() {
        return "PdbSequence{" +
                "pdbId='" + pdbId + '\'' +
                ", pdbSequence='" + pdbSequence + '\'' +
                '}';
    }
}
