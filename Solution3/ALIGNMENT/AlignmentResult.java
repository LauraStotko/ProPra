package Solution3.ALIGNMENT;

public class AlignmentResult {
    private final String pdbId1;
    private final String pdbId2;
    private final double alignmentScore;
    private final String alignmentSeq1;
    private final String alignmentSeq2;

    public AlignmentResult(String pdbId1, String pdbId2, double alignmentScore, String alignmentSeq1, String alignmentSeq2) {
        this.pdbId1 = pdbId1;
        this.pdbId2 = pdbId2;
        this.alignmentScore = alignmentScore;
        this.alignmentSeq1 = alignmentSeq1;
        this.alignmentSeq2 = alignmentSeq2;
    }

    public String getPdbId1() {
        return pdbId1;
    }

    public String getPdbId2() {
        return pdbId2;
    }

    public double getAlignmentScore() {
        return alignmentScore;
    }

    public String getAlignmentSeq1() {
        return alignmentSeq1;
    }

    public String getAlignmentSeq2() {
        return alignmentSeq2;
    }
}